#!/usr/bin/python3
"""Place Module for HBNB project."""
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy import MetaData
from sqlalchemy.orm import relationship

from models.base_model import BaseModel


place_amenity = Table(
    'place_amenity',
    MetaData(),
    Column(
        'place_id',
        String(60),
        ForeignKey('places.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    ),
    Column(
        'amenity_id',
        String(60),
        ForeignKey('amenities.id', onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True
    )
)


class Place(BaseModel):
    """A place to stay."""

    __tablename__ = 'places'

    city_id = Column(
        String(60),
        ForeignKey('cities.id'),
        nullable=False,
        default=''
    )
    user_id = Column(
        String(60),
        ForeignKey('users.id'),
        nullable=False,
        default=''
    )
    name = Column(
        String(128),
        nullable=False,
        default=''
    )
    description = Column(
        String(1024),
        nullable=True,
        default=''
    )
    number_rooms = Column(
        Integer,
        nullable=False,
        default=0
    )
    number_bathrooms = Column(
        Integer,
        nullable=False,
        default=0
    )
    max_guest = Column(
        Integer,
        nullable=False,
        default=0
    )
    price_by_night = Column(
        Integer,
        nullable=False,
        default=0
    )
    latitude = Column(
        Float,
        nullable=True,
        default=0.0
    )
    longitude = Column(
        Float,
        nullable=True,
        default=0.0
    )

    amenities = relationship(
        'Amenity',
        secondary=place_amenity,
        backref='place_amenities'
    )

    @property
    def amenity_ids(self):
        """Return the list of amenity IDs."""
        return [amenity.id for amenity in self.amenities]

    @amenity_ids.setter
    def amenity_ids(self, amenity_ids):
        """Set the amenities from a list of amenity IDs."""
        from models.amenity import Amenity
        from models import storage

        self.amenities = []

        for amenity_id in amenity_ids:
            key = 'Amenity.{}'.format(amenity_id)
            amenity = storage.all(Amenity).get(key)
            if amenity is not None:
                self.amenities.append(amenity)
