from drf_spectacular.utils import extend_schema_view

from docs.api.cart import (
    cart_clear,
    cart_create,
    cart_list,
    cart_retrieve,
    item_create,
    item_decrement,
    item_destroy,
    item_increment,
    item_list,
    item_partial_update,
    item_retrieve,
    item_update,
)

cart_item_schema = extend_schema_view(
    list=item_list.list_schema,
    create=item_create.create_schema,
    retrieve=item_retrieve.retrieve_schema,
    update=item_update.update_schema,
    partial_update=item_partial_update.partial_update_schema,
    destroy=item_destroy.destroy_schema,
    increment=item_increment.increment_schema,
    decrement=item_decrement.decrement_schema,
)


cart_schema = extend_schema_view(
    list=cart_list.list_schema,
    create=cart_create.create_schema,
    retrieve=cart_retrieve.retrieve_schema,
    clear=cart_clear.clear_schema,
)
