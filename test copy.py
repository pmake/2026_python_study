def test(list_of_int: list[int] ,type_to_sum: str='even',sum_start_ind: int=0):
    """加總傳入的清單

    Args:
        list_of_int (int): 整數清單
        type_to_sum (str, optional): 指定要加總奇數或偶數. Defaults to 'even'.
        sum_start_ind (int, optional): 指定從第幾個位置開始加總. Defaults to 0.

    Returns:
        tuple: 回傳兩層元組，結構: ((參數2,參數3),(指定類別加總, 清單加總, 指定個數加總))
    """
    remainder = 1 if type_to_sum == 'odd' else 0
    sum_of_assigned_type = 0
    sum_of_li = 0
    sum_of_last_three= 0
    try:
        sum_of_li = sum(list_of_int)
        sum_of_last_three = sum(list_of_int[sum_start_ind:])
        for el in list_of_int:
            if el % 2 == remainder:
                sum_of_assigned_type += el
    except Exception as e:
        print(f'something went wrong: {e}')
        print(f'請輸入整數')
    

    return (type_to_sum, sum_start_ind),(sum_of_assigned_type, sum_of_li, sum_of_last_three)
    
        



a, b = test([1,2,3,4,5,6],'even',2)
print(f'{a[0]}加總:', b[0])
print(f'清單加總:', b[1])
print(f'最後指定個數加總:', b[2])