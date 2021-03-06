# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    response.flash = T("Welcome to Streamline!")

    total_shipment = db().select(db.shipment.ALL)

    return dict(total_shipment=total_shipment)


def new_shipment():
    response.flash = T("Total shipment!")

    form = SQLFORM.factory(
        Field('date_shipment', type="date", requires=IS_NOT_EMPTY(error_message=T('Cannot be empty'))),
        Field('volume_transported', type="double", requires=IS_NOT_EMPTY(error_message=T('Cannot be empty'))),
        Field('distance_ship', type="double", requires=IS_NOT_EMPTY(error_message=T('Cannot be empty'))),
        Field('minimum_distance_ship', type="double", requires=IS_NOT_EMPTY(error_message=T('Cannot be empty'))),
        Field('value_meter_km', type="double", requires=IS_NOT_EMPTY(error_message=T('Cannot be empty'))),
        )

    if form.process().accepted:

        id = db.shipment.insert(
            volume_transported = form.vars.volume_transported,
            distance_ship = form.vars.distance_ship,
            minimum_distance_ship = form.vars.minimum_distance_ship,
            value_meter_km = form.vars.value_meter_km,
            )
        # response.flash = T("form accepted")
        redirect(URL("index"))
    elif form.errors:
        response.flash = T("form has errors")

    return dict(form=form)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in 
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
