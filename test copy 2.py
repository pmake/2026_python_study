class Smartphone:
    def __init__(self, brand: str, cost: int):
        self.brand: str = brand          # 公開屬性 (Public)
        self._warranty: int = 12         # 受保護屬性 (Protected，單底線，靠默契維護)
        self.__cost: int = cost          # 私有屬性 (Private，雙底線，啟動名稱修飾)

    def get_cost(self) -> int:
        """類別內部的方法，可以自由存取私有屬性"""
        return self.__cost


# --- 外部測試 ---
phone = Smartphone("Apple", 30000)

print(phone.brand)      # 正常輸出: Apple
print(phone._warranty)  # 正常輸出: 12 (雖然有警告，但抓得到)

# ❌ 嘗試直接存取私有屬性
print(phone.get_cost)   
# 💥 噴錯：AttributeError: 'Smartphone' object has no attribute '__cost'