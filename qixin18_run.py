from Sprider.Qixin18 import QiXin18

if __name__ == "__main__":
    cookies_str = r"beidoudata2015jssdkcross=%7B%22distinct_id%22%3A%22174ce902d06791-06a4af140aa4b4-37c143e-2073600-174ce902d071d6%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%7D%2C%22%24device_id%22%3A%22174ce902d06791-06a4af140aa4b4-37c143e-2073600-174ce902d071d6%22%7D; orderTips=true; acw_tc=2f6a1f8616040233482945646e3ca515f8a7302e0a2a664e1517cb94f61463; qx_trip_pc_sid=s%3AjzlaDx-ekdVZvc6NgsNfL7vierysHfA5.QOdhpuYNcXlf4o%2F%2BnVT98gXF%2FzMPM1KazYScCQR83%2FI; hz_guest_key=Spi0LT0OHZYKMH6J5D_1603696428681_3_0_0; env=preview; hz_visit_key=2KPzIUw77HZ1n7PSvkdG_1604023347842_5_1604023347842; hz_view_key=Spi0LT0OHZYKMH6J5D2Z1QXHaPpHZ1clVNdAgk_1604023384857_https%253A%252F%252Fwww.qixin18.com%252Fgoods%253Fis_from_new_merchant_pc%253Dtrue; auth-tips=1"
    QiXin18 = QiXin18(cookies_str)
    QiXin18.run()