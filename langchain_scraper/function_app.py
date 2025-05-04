################################################################################ BAREBONES TEST APP 1 ##############################################################################################

# import azure.functions as func

# app = func.FunctionApp()

# @app.route(route="hello", auth_level=func.AuthLevel.Function)
# def hello(req: func.HttpRequest) -> func.HttpResponse:
#     return func.HttpResponse("Hello from Azure Function!")

################################################################################ BAREBONES TEST APP 2 ##############################################################################################

import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="HttpExample")
def HttpExample(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

################################################################################ BAREBONES TEST APP END ##############################################################################################




# import azure.functions as func
# from azurefunctions.extensions.http.fastapi import Request, StreamingResponse #(suggested in documentation)
# from langchain.document_loaders import WebBaseLoader
# from azure.storage.blob import BlobServiceClient
# import os
# import datetime
# import json
# import logging

# app = func.FunctionApp()

# # @app.route(route="scrapeToBlob", auth_level=func.AuthLevel.Function)
# # def scrapeToBlob(req: func.HttpRequest) -> func.HttpResponse:

# @app.route(route="scrapeToBlob", auth_level=func.AuthLevel.Function)
# def scrapeToBlob(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info("LangChain scraping function triggered.")

#     url = req.params.get('url')
#     if not url:
#         return func.HttpResponse("Please pass a 'url' query parameter.", status_code=400)

#     try:
#         loader = WebBaseLoader(url)
#         docs = loader.load()

#         connect_str = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
#         container_name = os.environ.get("AZURE_BLOB_CONTAINER")
#         if not connect_str or not container_name:
#             raise Exception("Missing AZURE_STORAGE_CONNECTION_STRING or AZURE_BLOB_CONTAINER--environment variables")

#         blob_service_client = BlobServiceClient.from_connection_string(connect_str)
#         container_client = blob_service_client.get_container_client(container_name)

#         for i, doc in enumerate(docs):
#             blob_name = f"scraped_{i}.txt"
#             container_client.upload_blob(name=blob_name, data=doc.page_content, overwrite=True)  #NEW BIT OF CODE THAT SUPERCEDES THE BELOW 2 COMMENTED OUT LINES
#             # blob_client = container_client.get_blob_client(blob_name)
#             # blob_client.upload_blob(doc.page_content, overwrite=True)

#         return func.HttpResponse(f"Successfully scraped and uploaded {len(docs)} documents from {url}.")

#     except Exception as e:
#         logging.error(str(e))
#         return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)

#     # logging.info('Python HTTP trigger function processed a request.')

#     # name = req.params.get('name')
#     # if not name:
#     #     try:
#     #         req_body = req.get_json()
#     #     except ValueError:
#     #         pass
#     #     else:
#     #         name = req_body.get('name')

#     # if name:
#     #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     # else:
#     #     return func.HttpResponse(
#     #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#     #          status_code=200
#     #     )