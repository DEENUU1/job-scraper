from pydantic import BaseModel


class OfferStatusUpdate(BaseModel):
    """
    Represents data required to update the status of an offer.

    Attributes:
        offer_id (int): The unique identifier of the offer to be updated.
        status (bool): The new status of the offer. True indicates the offer is checked, False indicates unchecked.
    """

    offer_id: int
    status: bool
