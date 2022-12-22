""" MongoDB FastAPI """
import json
import pymongo
from pymongo.errors import PyMongoError
from pydantic import BaseModel, ValidationError
from fastapi import FastAPI, status, HTTPException

######### JSON SCHEMAS #########
class ItemIn(BaseModel):
    """Item In JSON Schema"""

    name: str
    price: int


class ItemOut(BaseModel):
    """Item Out JSON Schema"""

    status: int
    message: str
    docid: str
    docdata: dict


class ItemOutAll(BaseModel):
    """Item Out JSON Schema"""

    status: int
    message: str
    docdata: list


class ItemUpdate(BaseModel):
    """Item Update JSON Schema"""

    inputdoc: ItemIn
    outputdoc: ItemIn


class HTTPError(BaseModel):
    """HTTP Error JSON Schema"""

    detail: str


####### FASTAPI SETTINGS #######
app = FastAPI(
    title="Project",
    description="Project Description",
    openapi_tags=[
        {
            "name": "Inventory",
            "description": "These are items that are in your collection.",
        },
    ],
)

####### MONGODB SETTINGS #######
mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongodb = mongoclient["customer1"]
inventory = mongodb["inventory"]

####### CREATE A NEW DOC #######
@app.post(
    "/inventory/create/",
    tags=["Inventory"],
    response_model=ItemOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": HTTPError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": HTTPError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPError},
    },
)
async def create_inventory(create_json: ItemIn):
    """
    Create a new item in the Inventory Collection.
    """
    try:
        find_doc = inventory.find_one(create_json.dict())

    except PyMongoError as mongo_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=mongo_error
        ) from mongo_error

    if find_doc is None:
        try:
            create_doc = inventory.insert_one(create_json.dict())
            return ItemOut(
                status=status.HTTP_201_CREATED,
                message="Item created in inventory",
                docid=str(create_doc.inserted_id),
                docdata=create_json,
            )

        except PyMongoError as mongo_error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=mongo_error
            ) from mongo_error

    if find_doc is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Item already exists in Inventory",
        )


####### GET SINGLE DOC #########
@app.get(
    "/inventory/getone/",
    tags=["Inventory"],
    response_model=ItemOut,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": HTTPError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPError},
    },
)
async def read_inventory(find_json):
    """
    Retrieve a single item from the Inventory Collection.

    Please note that this is a string fed in instead of a request body,
    because the new OpenAPI is disallowing request bodies in HTTP GET
    going forward.

    { "name": "string", "price": 0 }
    """
    try:
        validate_json = json.loads(find_json)

    except ValueError as json_error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=json_error
        ) from json_error

    try:
        ItemIn.parse_obj(validate_json)

    except ValidationError as json_error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=json_error
        ) from json_error

    try:
        find_doc = inventory.find_one(validate_json)

    except PyMongoError as mongo_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=mongo_error
        ) from mongo_error

    if find_doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item doesn't exist in Inventory.",
        )

    if find_doc is not None:
        find_docid = str(find_doc["_id"])
        del find_doc["_id"]
        return ItemOut(
            status=status.HTTP_200_OK,
            message="Found in Inventory.",
            docid=find_docid,
            docdata=find_doc,
        )


######### GET ALL DOCS #########
@app.get(
    "/inventory/getall/",
    tags=["Inventory"],
    response_model=ItemOutAll,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPError}},
)
async def all_inventory():
    """Get all items in inventory collection."""
    try:
        all_docs = inventory.find({}, {"_id": 0})

    except PyMongoError as mongo_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=mongo_error
        ) from mongo_error

    doc_list = []

    for docs in all_docs:
        doc_list.append(docs)

    return ItemOutAll(
        status=status.HTTP_200_OK, message="All items in inventory.", docdata=doc_list
    )


####### SEARCH ALL KEYS ########
@app.get(
    "/inventory/search/{search_query}",
    tags=["Inventory"]
    ## updates here
)
async def search_inventory(search_query):
    """Search an entire collection in each key"""
    try:
        all_docs = inventory.find({}, {"_id": 0})

    except PyMongoError as mongo_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=mongo_error
        ) from mongo_error

    search_results = []

    for docs in all_docs:
        for items in list(docs.values()):
            if search_query in str(items):
                search_results.append(docs)

    return ItemOutAll(
        status=status.HTTP_200_OK,
        message="All items in inventory.",
        docdata=search_results,
    )


###### UPDATE SINGLE DOC #######
@app.put(
    "/inventory/update/",
    tags=["Inventory"],
    response_model=ItemOut,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": HTTPError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPError},
    },
)
async def update_inventory(update_json: ItemUpdate):
    """Update a document in collection"""
    update_input = update_json.dict()["inputdoc"]
    update_output = update_json.dict()["outputdoc"]

    try:
        find_input = inventory.find_one(update_input)
        find_output = inventory.find_one(update_output)

    except PyMongoError as mongo_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=mongo_error
        ) from mongo_error

    if find_input is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item doesn't exist in Inventory.",
        )

    if find_output is not None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Update info already exists in Inventory.",
        )

    try:
        update_query = {"$set": update_output}
        inventory.update_one(update_input, update_query)
        updated_item = inventory.find_one(update_output)
        updated_docid = str(updated_item["_id"])
        del updated_item["_id"]
        return ItemOut(
            status=status.HTTP_200_OK,
            message="Item Updated",
            docid=updated_docid,
            docdata=updated_item,
        )

    except PyMongoError as mongo_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=mongo_error
        ) from mongo_error


###### DELETE SINGLE DOC #######
@app.delete(
    "/inventory/delete/",
    tags=["Inventory"],
    response_model=ItemOut,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": HTTPError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": HTTPError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": HTTPError},
    },
)
async def delete_inventory(delete_json: ItemIn):
    """Delete a document in inventory collection"""
    delete_input = delete_json.dict()

    try:
        find_doc = inventory.find_one(delete_input)
        find_id = find_doc["_id"]

    except PyMongoError as mongo_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=mongo_error
        ) from mongo_error

    if find_doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item doesn't exist in Inventory.",
        )

    try:
        inventory.delete_one(delete_input)
        check_delete = inventory.find(find_id)

    except PyMongoError as mongo_error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=mongo_error
        ) from mongo_error

    if check_delete is not None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB Error"
        )

    if check_delete is None:
        return ItemOut(
            status=status.HTTP_200_OK,
            message="Item Deleted",
            docid=str(find_id),
            docdata=delete_input,
        )
