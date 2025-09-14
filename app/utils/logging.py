import structlog, logging, sys, os
from app.config.settings import settings

def relative_path(path):
    try:
        cwd = os.getcwd()
        return os.path.relpath(path, cwd)
    except Exception:
        return path

def add_relative_path(logger, method_name, event_dict):
    if "pathname" in event_dict:
        event_dict["pathname"] = relative_path(event_dict["pathname"])
    return event_dict

def configure_logging():
    logging.basicConfig(stream=sys.stdout, level=getattr(logging, settings.LOG_LEVEL, logging.INFO))
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,  # Adds log level
            structlog.processors.CallsiteParameterAdder([
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.PATHNAME,   # Adds file path
                structlog.processors.CallsiteParameter.LINENO,     # Adds line number
                structlog.processors.CallsiteParameter.MODULE,     # Adds module name
            ]),
            add_relative_path,  # Convert full path to relative
            structlog.dev.ConsoleRenderer(),
        ]
    )
    
# Example of a custom processor to log to MongoDB  
#     import structlog, logging, sys
# from app.config.settings import settings
# from pymongo import MongoClient

# class MongoDBLogProcessor:
#     def __init__(self, uri, db_name, collection_name):
#         self.client = MongoClient(uri)
#         self.collection = self.client[db_name][collection_name]

#     def __call__(self, logger, method_name, event_dict):
#         # Insert the log event as a document
#         self.collection.insert_one(event_dict)
#         return event_dict

# def configure_logging():
#     logging.basicConfig(stream=sys.stdout, level=getattr(logging, settings.LOG_LEVEL, logging.INFO))
#     mongo_processor = MongoDBLogProcessor(
#         uri=settings.MONGO_URI,
#         db_name=settings.MONGO_DB,
#         collection_name="logs"
#     )
#     structlog.configure(
#         processors=[
#             structlog.processors.TimeStamper(fmt="iso"),
#             structlog.processors.add_log_level,
#             structlog.processors.CallsiteParameterAdder([
#                 structlog.processors.CallsiteParameter.FUNC_NAME,
#                 structlog.processors.CallsiteParameter.PATHNAME,
#                 structlog.processors.CallsiteParameter.LINENO,
#                 structlog.processors.CallsiteParameter.MODULE,
#             ]),
#             mongo_processor,  # Store log in MongoDB
#             structlog.processors.JSONRenderer(),
#         ]
#     )