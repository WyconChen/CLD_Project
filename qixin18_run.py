from Sprider.Qixin18 import QiXin18

if __name__ == "__main__":
    cookies_str = r"orderTips=true; auth-tips=1; beidoudata2015jssdkcross=%7B%22distinct_id%22%3A%22174ce902d06791-06a4af140aa4b4-37c143e-2073600-174ce902d071d6%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22174ce902d06791-06a4af140aa4b4-37c143e-2073600-174ce902d071d6%22%7D; acw_tc=2f6a1fde16043097986183986e37ff277cd5d7c35c150382a4d2dcc9c9edb5; qx_trip_pc_sid=s%3Aw1nUmGIrQaUVHauFwMND4O_-tzFEwUon.RavFbuZ9I5zIcDc7MriBMVg4MjZWm7MnlAJXv7zlcAc; hz_guest_key=1NcpD1kC6HZ2xpCY0Kf4_1604304031556_2_0_0; env=preview; hz_visit_key=1Q2t5aqUqHZDgy7OWW7_1604309799396_9_1604309799396; hz_view_key=1NcpD1kC6HZ2xpCY0Kf43de8vRPanHZ3bgL2liXc_1604309890687_https%253A%252F%252Fwww.qixin18.com%252Fgoods%253Fis_from_new_merchant_pc%253Dtrue"
    QiXin18 = QiXin18(cookies_str)
    QiXin18.run()