import time
import logging
import sqlalchemy
from sqlalchemy.orm import Session

from ..parse.sparx_db import TPackage
from ..generate import generate

from mdg.config import settings

logger = logging.getLogger(__name__)


def poller(duration):
    engine = sqlalchemy.create_engine(f"{settings['source']}", echo=False, future=True, isolation_level="READ UNCOMMITTED")
    with Session(engine) as session:
        done = False
        version = None

        # Find the package with the model nodes. Can specify either EA GUID or name
        # If guid make sure value in recipie is quoted - model_package: "{D6D3BF36-E897-4a8b-8CA9-62ADAAD696ED}"
        if settings['model_package'][0] == "{":
            stmt = sqlalchemy.select(TPackage).where(TPackage.ea_guid == settings['model_package'])
        else:
            stmt = sqlalchemy.select(TPackage).where(TPackage.name == settings['model_package'])

        while not done:
            model_tpackage: TPackage = session.execute(stmt).scalars().first()
            session.commit()
            if model_tpackage is None:
                raise ValueError("Model package element not found. Settings has:{}".format(settings['model_package']))

            if version is not None and model_tpackage.version != version:
                logger.info(f"Detected version change in model package. Version {model_tpackage.version}")
                generate()

            version = model_tpackage.version
            time.sleep(duration)
