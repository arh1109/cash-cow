"""
Day 4 - Pydantic v2 Schema for the robot resource

What is Pydantic? A validation framework used widelyin python projects and other frameworks for validating
the shape of data, especially in transit.

Why is this separate from the models? The Models leverage ORM level definitions to define how
they interact with a database. We don't need to have all of that, this is going to be defining
the shape that gets passed in and out of the application.
"""

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ATMStatus

# Look at different fields in database with SELECT * from robots;
class ATMBase(BaseModel):
    serial_number: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=100)
    battery_level: Decimal = Field(ge=0, le=100)
    facility_id: int
    status: ATMStatus = ATMStatus.OPERATIONAL

# Two additional classes that build upon this starter class
class ATMCreate(ATMBase):
    """ Shape of the Request Body for POST /atms """

class ATMRead(ATMBase):
    """ Shape of a Robot in any API Response """
    id: int

    # Allows us to construct a RobotRead obj from the database.
    model_config = ConfigDict(from_attributes=True)