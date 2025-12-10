from infra.base_api import BaseApi

class StoreApi():

    def get_store_inventory(self):
        return BaseApi.get_api_call('store/inventory')

    @staticmethod
    def get_store_order_id(ids):
        return BaseApi.get_api_call(f'store/order/{ids}')

    def create_store_order(self, order_data):
        return BaseApi.post_api_call('store/order', order_data)

    def delete_store_order(self, order_id):
        return BaseApi.delete_api_call(f'store/order/{order_id}')