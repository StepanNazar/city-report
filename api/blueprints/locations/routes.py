import requests
from apiflask import abort
from apiflask.views import MethodView
from flask_jwt_extended import jwt_required

from api import db
from api.blueprints.common.schemas import pagination_query_schema
from api.blueprints.locations import locations
from api.blueprints.locations.schemas import (
    CountryPaginationSchema,
    CountrySchema,
    LocalityPaginationSchema,
    LocalitySchema,
    LocationNameInputSchema,
    StatePaginationSchema,
    StateSchema,
)
from api.services import LocationService


class Countries(MethodView):
    @locations.input(pagination_query_schema(200, 200), location="query")
    @locations.output(CountryPaginationSchema)
    def get(self, query_data):
        """Get all countries"""
        return {}, 501

    @jwt_required()
    @locations.input(LocationNameInputSchema)
    @locations.output(CountrySchema, status_code=201)
    @locations.doc(security="jwt_access_token", responses={201: "Country created"})
    def post(self):
        """Create a new country. Activated account required."""
        return {}, 501


class Country(MethodView):
    @locations.output(CountrySchema)
    def get(self, country_id):
        """Get a country by ID"""
        return {}, 501


class CountryStates(MethodView):
    @locations.input(pagination_query_schema(50, 200), location="query")
    @locations.output(StatePaginationSchema)
    def get(self, country_id, query_data):
        """Get all states for the country"""
        return {}, 501

    @jwt_required()
    @locations.input(LocationNameInputSchema)
    @locations.output(StateSchema, status_code=201)
    @locations.doc(
        security="jwt_access_token", responses={201: "State created for the country"}
    )
    def post(self, country_id):
        """Create a new state for the country. Activated account required."""
        return {}, 501


class States(MethodView):
    @locations.input(pagination_query_schema(50, 200), location="query")
    @locations.output(StatePaginationSchema)
    def get(self, query_data):
        """Get all states"""
        return {}, 501


class State(MethodView):
    @locations.output(StateSchema)
    def get(self, state_id):
        """Get a state by ID"""
        return {}, 501


class StateLocalities(MethodView):
    @locations.input(pagination_query_schema(50, 200), location="query")
    @locations.output(LocalityPaginationSchema)
    def get(self, state_id, query_data):
        """Get all localities for the state"""
        return {}, 501

    @jwt_required()
    @locations.input(LocationNameInputSchema)
    @locations.output(LocalitySchema, status_code=201)
    @locations.doc(
        security="jwt_access_token", responses={201: "Locality created for the state"}
    )
    def post(self, state_id):
        """Create a new locality for the state. Activated account required."""
        return {}, 501


class Localities(MethodView):
    @locations.input(pagination_query_schema(50, 200), location="query")
    @locations.output(LocalityPaginationSchema)
    def get(self, query_data):
        """Get all localities"""
        return {}, 501


class Locality(MethodView):
    @locations.output(LocalitySchema)
    def get(self, locality_id):
        """Get a locality by ID"""
        return {}, 501


# URL rules
locations.add_url_rule("/countries", view_func=Countries.as_view("countries"))
locations.add_url_rule(
    "/countries/<int:country_id>", view_func=Country.as_view("country")
)
locations.add_url_rule(
    "/countries/<int:country_id>/states",
    view_func=CountryStates.as_view("country_states"),
)

locations.add_url_rule("/states", view_func=States.as_view("states"))
locations.add_url_rule("/states/<int:state_id>", view_func=State.as_view("state"))
locations.add_url_rule(
    "/states/<int:state_id>/localities",
    view_func=StateLocalities.as_view("state_localities"),
)

locations.add_url_rule("/localities", view_func=Localities.as_view("localities"))
locations.add_url_rule(
    "/localities/<int:locality_id>", view_func=Locality.as_view("locality")
)


def get_or_create_locality(locality_id, locality_provider):
    try:
        return LocationService.get_or_create_locality(
            locality_id, locality_provider, db.session
        )
    except ValueError:
        abort(400, message="Invalid locality id")
    except requests.RequestException:
        abort(500, message="Location service unavailable")
    except NotImplementedError as e:
        abort(501, message=str(e))
