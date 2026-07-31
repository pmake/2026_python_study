import pandas as pd

def calculate_transit_minutes(df_employee_day: pd.DataFrame) -> int:
    """
    同日同保母按排班時間排序，計算轉場加時（分鐘）。
    同日相鄰兩筆服務居住地址不同，每次切換加算 15 分鐘。
    """
    if len(df_employee_day) <= 1:
        return 0
    
    # 依排班時間排序
    df_sorted = df_employee_day.sort_values(by='排班時間')
    addresses = df_sorted['居住地址'].tolist()
    
    transit_count = 0
    for i in range(1, len(addresses)):
        if addresses[i] != addresses[i - 1]:
            transit_count += 1
            
    return transit_count * 15


def segment_daily_hours(total_minutes: int, is_holiday: bool, emp_category: str) -> dict:
    """
    依當日總工時（服務工時+轉場加時，單位：分鐘）及員工類別、假日屬性，區分各類工時切片（單位：分鐘）。
    """
    res = {
        '正常工時': 0,
        '平日加班_9_10h': 0,
        '平日加班_11_12h': 0,
        '平日轉場加時': 0,
        '假日工時_0_2h': 0,
        '假日工時_3_12h': 0,
        '假日轉場加時': 0,
    }
    
    # Cap total billable minutes at 12h (720 minutes)
    billable_minutes = min(total_minutes, 720)
    
    if emp_category == '假日班':
        if is_holiday:
            res['假日工時_0_2h'] = min(billable_minutes, 120)
            res['假日工時_3_12h'] = max(0, billable_minutes - 120)
        else:
            res['正常工時'] = billable_minutes
    else:  # 常日班
        if is_holiday:
            res['假日工時_0_2h'] = min(billable_minutes, 120)
            res['假日工時_3_12h'] = max(0, billable_minutes - 120)
        else:
            res['正常工時'] = min(billable_minutes, 480)
            if billable_minutes > 480:
                res['平日加班_9_10h'] = min(billable_minutes - 480, 120)
            if billable_minutes > 600:
                res['平日加班_11_12h'] = min(billable_minutes - 600, 120)
                
    return res


def run_tests():
    print("=== 開始執行單元測試 ===")
    
    # 測試1: A -> B -> A 轉場 30m
    df1 = pd.DataFrame({
        '排班時間': ['09:00', '11:00', '14:00'],
        '居住地址': ['地址A', '地址B', '地址A']
    })
    assert calculate_transit_minutes(df1) == 30, "測試1失敗"
    print("[PASS] 轉場測試: A->B->A 正確計算 30 分鐘")

    # 測試2: 同地址連續服務 轉場 0m
    df2 = pd.DataFrame({
        '排班時間': ['09:00', '11:00'],
        '居住地址': ['地址A', '地址A']
    })
    assert calculate_transit_minutes(df2) == 0, "測試2失敗"
    print("[PASS] 轉場測試: 同地址連續服務 正確計算 0 分鐘")

    # 測試3: 常日班平日 13小時
    res3 = segment_daily_hours(780, is_holiday=False, emp_category='常日班')
    assert res3['正常工時'] == 480 and res3['平日加班_9_10h'] == 120 and res3['平日加班_11_12h'] == 120, "測試3失敗"
    print("[PASS] 工時分段測試: 常日班平日超過 12h 正確封頂計算")

    # 測試4: 常日班假日 5小時
    res4 = segment_daily_hours(300, is_holiday=True, emp_category='常日班')
    assert res4['假日工時_0_2h'] == 120 and res4['假日工時_3_12h'] == 180, "測試4失敗"
    print("[PASS] 工時分段測試: 常日班假日正確切分 0-2h 與 3-12h")

    # 測試5: 假日班假日 10小時
    res5 = segment_daily_hours(600, is_holiday=True, emp_category='假日班')
    assert res5['假日工時_0_2h'] == 120 and res5['假日工時_3_12h'] == 480, "測試5失敗"
    print("[PASS] 工時分段測試: 假日班假日正確切分")

    print("=== 所有單元測試皆 100% 通過 ===")

if __name__ == '__main__':
    run_tests()
