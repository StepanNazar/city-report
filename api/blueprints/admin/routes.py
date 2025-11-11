from flask.views import MethodView
from flask_jwt_extended import jwt_required

from api.blueprints.admin import admin
from api.blueprints.admin.schemas import (
    CreateAdminSchema,
    ReportPaginationSchema,
    ReportSchema,
    ReportSortingFilteringSchema,
)
from api.blueprints.common.schemas import merge_schemas, pagination_query_schema
from api.blueprints.users.schemas import UserOutPaginationSchema, UserOutSchema


class Reports(MethodView):
    @jwt_required()
    @admin.input(
        merge_schemas(pagination_query_schema(), ReportSortingFilteringSchema),
        location="query",
    )
    @admin.output(ReportPaginationSchema)
    @admin.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "Reports retrieved"},
    )
    def get(self, query_data):
        """Get all reports. Ordered by report time."""
        return {}, 501


class Report(MethodView):
    @jwt_required()
    @admin.output(ReportSchema)
    @admin.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "Report retrieved"},
    )
    def get(self, report_id):
        """Get report by ID"""
        return {}, 501


class ReportApproval(MethodView):
    @jwt_required()
    @admin.doc(
        security="jwt_access_token",
        responses={204: "Report approved", 403: "Forbidden"},
    )
    def put(self, report_id):
        """Approve the report. Delete the corresponding post / comment / solution."""
        return {}, 501


class ReportDisapproval(MethodView):
    @jwt_required()
    @admin.doc(
        security="jwt_access_token",
        responses={204: "Report disapproved", 403: "Forbidden"},
    )
    def put(self, report_id):
        """Disapprove report. Undelete the corresponding post / comment / solution."""
        return {}, 501


class Admins(MethodView):
    @jwt_required()
    @admin.input(pagination_query_schema(), location="query")
    @admin.output(UserOutPaginationSchema)
    @admin.doc(
        security="jwt_access_token",
        responses={403: "Forbidden", 200: "Admins retrieved"},
    )
    def get(self, query_data):
        """Get all admins"""
        return {}, 501

    @jwt_required()
    @admin.input(CreateAdminSchema)
    @admin.output(UserOutSchema, status_code=201)
    @admin.doc(
        security="jwt_access_token", responses={403: "Forbidden", 201: "Admin created"}
    )
    def post(self):
        """Give admin rights to user. Password is required."""
        return {}, 501


admin.add_url_rule("/reports", view_func=Reports.as_view("reports"))
admin.add_url_rule("/reports/<int:report_id>", view_func=Report.as_view("report"))
admin.add_url_rule(
    "/reports/<int:report_id>/approval",
    view_func=ReportApproval.as_view("report_approval"),
)
admin.add_url_rule(
    "/reports/<int:report_id>/disapproval",
    view_func=ReportDisapproval.as_view("report_disapproval"),
)

admin.add_url_rule("/admins", view_func=Admins.as_view("admins"))
