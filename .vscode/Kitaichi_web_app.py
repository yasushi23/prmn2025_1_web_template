#ミリしらでもわかる！ポケモンバトルシミュレーション！
from flask import Flask, render_template,request
app = Flask(__name__)

class Pokemon:

    def __init__(self,name,hp,level,type):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.level = level
        self.type = type

    def attack(self, target,skill_index):
        skill = list(self.damage.keys())[skill_index]
        skill_type = skill[1]
        skill_name = skill[0]

        effectiveness = type_effectiveness(skill_type, target.type)

        target.hp -= self.damage[skill] * effectiveness
        print(self.name + "の" + skill_name + "!")

        if effectiveness == 2.0:
            print("こうかは  ばつぐんだ！")
        elif effectiveness == 0.5:
            print("こうかは  いまひとつのようだ・・・")
        
        
              

    def show_status(self):
        print("[" + self.name + ":Lv." + str(self.level) + "]HP:" + str(self.hp) + "/" + str(self.max_hp))
#ピカチュウ
class Pikachu(Pokemon):
    def __init__(self):
        super().__init__("ピカチュウ", 100, 5, "でんき")
        self.damage = {("10まんボルト", "でんき"): 25, ("でんこうせっか", "でんき"): 15, ("ほっぺすりすり", "でんき"): 10, ("アイアンテール", "はがね"): 20}

#ヒトカゲ
class Hitokage(Pokemon):
    def __init__(self):
        super().__init__("ヒトカゲ", 90, 5, "ほのお")
        self.damage = {("ひのこ", "ほのお"): 25, ("ひっかく", "ノーマル"): 15, ("かみくだく", "あく"): 20, ("とっしん", "ノーマル"): 10}
#ゼニガメ
class Zenigame(Pokemon):
    def __init__(self):
        super().__init__("ゼニガメ", 95, 5, "みず")
        self.damage = {("みずでっぽう", "みず"): 25, ("こうそくスピン", "ノーマル"): 20, ("たいあたり", "ノーマル"): 15, ("かみつく", "あく"): 20}
#フシギダネ
class Fushigidane(Pokemon):
    def __init__(self):
        super().__init__("フシギダネ", 90, 5, "くさ")
        self.damage = {("つるのムチ", "くさ"): 25, ("はっぱカッター", "くさ"): 20, ("ねむりごな", "くさ"): 0, ("こうごうせい", "くさ"): 0}
#ライチュウ
class Raichu(Pokemon):
    def __init__(self):
        super().__init__("ライチュウ", 200, 5, "でんき")
        self.damage = {("10まんボルト", "でんき"): 35, ("かみなり", "でんき"): 50, ("でんじは", "でんき"): 0, ("エレキボール", "でんき"): 25}

#ポケモンリスト
pokemon_list = [Pikachu(), Hitokage(), Zenigame(), Fushigidane(), Raichu()]



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select', methods=['GET', 'POST'])
def select():
    if methods == 'POST':
        pokemon_index = int(request.from['pokemon'])
        user_pokemon = pokemon_list[pokemon_index]

        return render_template('battle.html', user_pokemon = user_pokemon )
        
    return render_template('select.html')

@app.route('/battle')
def battle():
    return render_template('battle.html')

@app.route('/result')
def result():
    return render_template('result.html')