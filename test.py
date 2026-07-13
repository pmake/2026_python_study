# =============================================================================
# Python 物件導向（OOP）完整架構範例
# =============================================================================

class Animal:
    """
    這是父類別（基底類別 Base Class）
    定義了動物的共通屬性與行為。
    """
    # 類別屬性（Class Attribute）：所有實例共享
    species_kingdom: str = "Animalia"

    def __init__(self, name: str, age: int):
        """
        初始化方法（建構子 Constructor）
        當建立新物件時會自動呼叫，用來設定實例屬性。
        """
        # 實例屬性（Instance Attributes）：每個物件各自獨立
        self.name: str = name
        self.age: int = age
        
        # 加上單底線 '_' 代表受保護的屬性（Protected），內規上不建議外部直接存取
        self._is_hungry: bool = True
        
        # 加上雙底線'__' 私有屬性，不過Python 的私有屬性背後的運作機制非常有趣，
        # 它採取了一種叫做 「名稱修飾（Name Mangling）」 的溫和做法，
        # 而不是像 Java 或 C++ 那樣從底層強制鎖死。簡單說，它只是偷偷改名，改法規則一致，
        # 當 Python 看到你定義了 __cost 時，它在底層會偷偷把這個名字改掉，公式是：
                # _類別名__屬性名，直接用__cost無法存取，但用_類別名__cost就可以存取
                # 所以社群更推單底線方式
        self.__cost: int = 3000
                
        # @property 裝飾器：將方法偽裝成「屬性」來存取（Getter的角色）
        # 具體運作方式後面會說明
    @property
    def animal_info(self) -> str:
        """優雅地獲取動物的資訊"""
        return f"名字: {self.name}, 年齡: {self.age} 歲"
    # 另一個getter
    @property
    def cost(self) -> int:
            return self.__cost
    
    # 搭配getter的setter 裝飾器宣告方式，格式為<getter name>.setter
    # 下一列對應的函式名稱也要相同
    @cost.setter
    def cost(self, value: int) -> None:
            if value > 0:
                self.__cost = value

    def make_sound(self) -> str:
        """實例方法（Instance Method）：第一個參數必須是 self，代表物件本身"""
        return "一些動物的叫聲..."

    def eat(self) -> None:
        """改變物件內部狀態的實例方法"""
        self._is_hungry = False
        print(f"[{self.name}] 正在吃東西，現在不餓了。")


# -----------------------------------------------------------------------------
# 繼承（Inheritance）與多型（Polymorphism）
# -----------------------------------------------------------------------------

class Dog(Animal):
    """
    這是子類別（衍生類別 Derived Class），繼承自 Animal
    """
    def __init__(self, name: str, age: int, breed: str):
        """子類別的建構子"""
        # 使用 super() 呼叫父類別的建構子，初始化父類別定義好的屬性
        super().__init__(name, age)
        # 定義子類別特有的屬性
        self.breed: str = breed

    def make_sound(self) -> str:
        """
        方法覆寫（Method Overriding）：多型的展現
        覆寫父類別的 make_sound 方法，做出屬於狗的行為。
        """
        return "汪汪！"

# =============================================================================
# 實際使用範例（與物件互動）
# =============================================================================

if __name__ == "__main__":
    print("--- 1. 建立物件（實例化 Instantiation）---")
    # 建立 Dog 類別的實例（物件）
    my_dog = Dog(name="波比", age=3, breed="柴犬")

    print("--- 2. 存取屬性與呼叫方法 ---")
    # 存取類別屬性（透過類別或實例皆可）
    print(f"生物界別: {Dog.species_kingdom}") 
    
    # 使用 @property 屬性（注意：後面不用加括號 ()）
    print(my_dog.animal_info) 

    # 呼叫實例方法
    print(f"{my_dog.name} 的叫聲: {my_dog.make_sound()}")

    print("--- 3. 改變物件狀態 ---")
    # 呼叫從父類別繼承來的方法
    my_dog.eat()