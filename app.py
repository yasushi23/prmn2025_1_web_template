# ミリしらでもわかる！ポケモンバトルシミュレーション！
from flask import Flask, render_template, request, redirect, url_for, session
import random
app = Flask(__name__)
app.secret_key = 'pokemon-battle-secret'


#共通クラス　Pokemon
class Pokemon:

    def __init__(self, name, hp, level, type, image, description,
                 evolution_level=None, evolution_class=None):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.level = level
        self.type = type
        self.actable = 0
        self.image = image
        self.description = description

        #進化
        self.evolution_level = evolution_level
        self.evolution_class = evolution_class

    #ダメージ計算
    def attack(self, target, skill_index):
        skill = list(self.damage.keys())[skill_index]
        skill_type = skill[1]
        skill_name = skill[0]

        effectiveness = type_effectiveness(skill_type, target.type)

        message = self.name + "の" + skill_name + "!"

        if skill_name == 'こうごうせい':
            self.hp +=  30
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            message += self.name + "は体力を回復した！"
            

        elif skill_name == 'ねむりごな':
            target.actable = 1
            message += target.name +"は眠ってしまった！"
            

        elif skill_name == 'でんじは':
            target.actable = random.randrange(0,2)
            if target.actable == 1:
                message += target.name +"は痺れてうごけない！"

        elif skill_name == 'すてみタックル':
             self.hp -= 20
             message += self.name + "は、すてみタックルの反動ダメージをうけた！"
        
        else:
            target.hp -= self.damage[skill] * effectiveness

            if effectiveness == 2.0:
                message += "こうかは  ばつぐんだ！"
          
            elif effectiveness == 0.5:
                message += "こうかは  いまひとつのようだ・・・"

            message += str(self.damage[skill]*effectiveness) +"のダメージ！"

        return message
    
    #ステータス表示
    def show_status(self):
        print("[" + self.name + ":Lv." + str(self.level) + "]HP:" +
              str(self.hp) + "/" + str(self.max_hp))
        
    #進化　クラス入れ替え
    def evolve(self):
        if self.evolution_level is not None:
            if self.level >= self.evolution_level:
                return self.evolution_class()

        return self

# ピカチュウ
class Pikachu(Pokemon):
    def __init__(self):
        super().__init__("ピカチュウ", 100, 5, "でんき","pikachu.png",
                         "ねずみポケモン　ほっぺたの両側に小さい電気袋を持つ",
                         evolution_level=10,     
                         evolution_class=Raichu)
        
        self.damage = {("10まんボルト", "でんき"): 25, ("でんこうせっか", "でんき"): 15, ("ほっぺすりすり", "でんき"): 10, ("アイアンテール", "はがね"): 20}

   

# ヒトカゲ
class Hitokage(Pokemon):
    def __init__(self):
        super().__init__("ヒトカゲ", 90, 5, "ほのお", "hitokage.png",
                         "とかげポケモン　尻尾の炎はヒトカゲの生命力の証",
                         evolution_level=10,     
                         evolution_class=Rezerd)
        self.damage = {("ひのこ", "ほのお"): 25, ("ひっかく", "ノーマル"): 15,
                       ("かみくだく", "あく"): 20, ("とっしん", "ノーマル"): 10}

# ゼニガメ
class Zenigame(Pokemon):
    def __init__(self):
        super().__init__("ゼニガメ", 95, 5, "みず", "zenigame.png",
                         "かめのこポケモン　甲羅に閉じこもり身を守る",
                         evolution_level=10,     
                         evolution_class=Kamale)
        self.damage = {("みずでっぽう", "みず"): 25, ("こうそくスピン", "ノーマル"): 20, ("たいあたり", "ノーマル"): 15, ("かみつく", "あく"): 20}

# フシギダネ
class Fushigidane(Pokemon):
    def __init__(self):
        super().__init__("フシギダネ", 90, 5, "くさ", "fushigidane.png",
                         "たねポケモン　背中に不思議なタネが植えてあって体とともに育つという",
                         evolution_level=10,     
                         evolution_class=Fushigisou)
        self.damage = {("つるのムチ", "くさ"): 25, ("はっぱカッター", "くさ"): 20, ("ねむりごな", "くさ"): 0, ("こうごうせい", "くさ"): 0}

# ライチュウ
class Raichu(Pokemon):
    def __init__(self):
        super().__init__("ライチュウ", 200, 10, "でんき", "raichu.png",
                         "ねずみポケモン　ピカチュウが進化したポケモン。以前よりも攻撃的")
        self.damage = {("10まんボルト", "でんき"): 35, ("かみなり", "でんき"): 50, ("でんじは", "でんき"): 0, ("エレキボール", "でんき"): 25}

#リザード
class Rezerd(Pokemon):
    def __init__(self):
        super().__init__("リザード", 210, 10, "ほのお", "rezerd.png",
                         "かえんポケモン　ヒトカゲが進化したポケモン。鋭いツメで相手をズタズタにひきさいてしまう")
        self.damage = {("かえんほうしゃ", "ほのお"):40, ("ドラゴンクロー", "ドラゴン"):20, 
                       ("かみくだく", "あく"): 20, ("すてみタックル", "ノーマル"): 50}

#カメール
class Kamale(Pokemon):
     def __init__(self):
        super().__init__("カメール", 220, 10, "みず", "kamale.png",
                        "かめポケモン　ゼニガメが進化したポケモン。ポカンと頭を叩かれるとき、甲羅に引っ込んで避ける")
        self.damage = {("みずのはどう", "みず"): 40, ("しねんのずつき", "エスパー"): 30, ("れいとうビーム", "こおり"): 35, ("かみつく", "あく"): 20}

#フシギソウ
class Fushigisou(Pokemon):
     def __init__(self):
        super().__init__("フシギソウ", 200, 10, "くさ　どく", "fushigisou.png",
                         "たねポケモン　つぼみが背中についていて、養分を吸収していくと大きな花が咲くという")
        self.damage = {("タネばくだん", "くさ"): 25, ("ベノムショック", "どく"): 20, ("ねむりごな", "くさ"): 0, ("こうごうせい", "くさ"): 0}

#タイプ相性のダメージ調整
def type_effectiveness(attack_type, target_type):
    effectiveness = 1.0

    if attack_type == "でんき" and target_type == "みず":
        effectiveness = 2.0
    elif attack_type == "ほのお" and target_type == "くさ":
        effectiveness = 2.0
    elif attack_type == "ほのお" and target_type == "みず":
        effectiveness = 0.5
    elif attack_type == "みず" and target_type == "ほのお":
        effectiveness = 2.0
    elif attack_type == "みず" and target_type == "くさ":
        effectiveness = 0.5
    elif attack_type == "くさ" and target_type == "みず":
        effectiveness = 2.0
    elif attack_type == "くさ" and target_type == "ほのお":
        effectiveness = 0.5

    return effectiveness


# ポケモンリスト、ポケモンクラス、ポケモンクラスdict（用途別）
pokemon_list = [Pikachu(), Hitokage(), Zenigame(), Fushigidane(), Raichu(), Rezerd(), Kamale(), Fushigisou()]
pokemon_classes = [Pikachu, Hitokage, Zenigame, Fushigidane, Raichu, Rezerd, Kamale, Fushigisou]
pokemon_class_dict = {
    'ピカチュウ': Pikachu,
    'ヒトカゲ': Hitokage,
    'ゼニガメ': Zenigame,
    'フシギダネ': Fushigidane,
    'ライチュウ': Raichu,
    'リザード': Rezerd,
    'カメール': Kamale,
    'フシギソウ':Fushigisou
}
#index.html(タイトルメニュー)
@app.route('/')
def index():
    return render_template('index.html')

#(オーキド博士による説明)
@app.route('/description/<int:page>')
def description(page):

    descriptions = [
        {
            "title": "このシミュレーションについて",
            "text": "ちょりっす！わし、オーキド。みんなからはポケモン博士って呼ばれおる。早速だが、このシミュレーションについてまず説明するぞ！"
                    "このシミュレーションは、今までポケモンに触れたことのない逆張りポケモンミリしら野郎にむけて、ポケモンバトルとは何か、を体験してもらうぞ！"
                    "耳の穴かっぽじってよく聞けのじゃ！ちなみに、超簡易的システムなのでクオリティについての批判は受け付けないのでそこんとこよろしこ"
        },
        {
            "title": "ポケモンバトルとは？",
            "text": "ポケモンを使って相手のポケモンと戦うのじゃ！相手のHPを0にすれば勝利じゃぞ！"
        },
        {
            "title": "技を選ぼう！",
            "text": "バトルでは、ポケモンが覚えている技の中から1つを選んで攻撃することができるぞ。"
                    "技には攻撃技と特殊技があって、特殊技では様々な効果を出すことができるのじゃ"
        },
        {
            "title": "タイプ相性",
            "text": "ポケモンの技にはタイプがある。相手との相性によって、与えるダメージが変わるのじゃ！"
                    "ほのおタイプはくさタイプに強く、くさタイプはみずタイプに強く、みずタイプはほのおタイプにつよい！"
                    "他にも、でんきタイプはみずタイプに強かったり、こおりタイプはひこうタイプに強かったり・・・。"
                    "全18種の複雑なタイプ相性を把握することが、勝利への近道じゃぞ！"
        },
        {
            "title": "特殊な技",
            "text": "このシミュレーションで設定されている特殊技について、いくつか説明するぞ！"
                    "ねむりごなは相手を眠らせ、相手を行動不能にできるぞ。でんじはは相手を確率でまひさせることができる。こうごうせいは自分のHPを回復する技じゃ！"
        },
        {
            "title": "レベルアップ",
            "text": "バトルに勝利するとポケモンのレベルが上がるぞ！レベルが上がると最大HPも増えるのじゃ！"
                    "レベルがある値に達すると、ポケモンが進化することがあるぞ！今回はレベルが5上がると進化する仕様じゃから、試しに5回勝利してみてほしい"
        },
        {
            "title":"いかがだったかな？",
            "text":"今回は最も基礎的なことについて解説したぞ。"
                   "ポケモンバトルは奥が深い！ポケモンの数だけ戦い方があるのじゃ。"
                   "今回の説明で分からなかった奴はもう正規品買ってくれ。"
                   "それでは、ポケモンを選んでバトル開始じゃ！"
        }
    ]

    return render_template('description.html', 
                           description = descriptions[page], 
                           page=page,
                           max_page=len(descriptions)-1)

#selct(ポケモン選択)
@app.route('/select', methods=['GET', 'POST'])
def select():
    print("===== SELECT =====")
    print(dict(session))

    #ユーザー側のポケモン初期値
    if 'pokemon_data' not in session:
                session['pokemon_data'] = {'ピカチュウ': {'level': 5, 'max_hp': 100},
                                            'ヒトカゲ': {'level': 5, 'max_hp': 90},
                                            'ゼニガメ': {'level': 5, 'max_hp': 95},
                                            'フシギダネ': {'level': 5, 'max_hp': 90},
                                            'ライチュウ': {'level': 10, 'max_hp': 200}}
    #コンピューター側のポケモン初期値
    if 'computer_data' not in session:
                session['computer_data'] = {'ピカチュウ': {'level': 5, 'max_hp': 100},
                                            'ヒトカゲ': {'level': 5, 'max_hp': 90},
                                            'ゼニガメ': {'level': 5, 'max_hp': 95},
                                            'フシギダネ': {'level': 5, 'max_hp': 90},
                                            'ライチュウ': {'level': 10, 'max_hp': 200}}
    #ポケモンスロット（番号と名前をセット）
    if 'pokemon_slots' not in session:
                session['pokemon_slots'] = {
                                            '0': 'ピカチュウ',
                                            '1': 'ヒトカゲ',
                                            '2': 'ゼニガメ',
                                            '3': 'フシギダネ'}


    
    if request.method == 'POST':

        #インデックス（行動や名前を決める値を設定）
        pokemon_index = int(request.form['pokemon'])
        computer_index = random.randrange(0, 4)
        #sessionでインデックスを復元
        session['pokemon_index'] = pokemon_index
        session['computer_index'] = computer_index

        #ポケモンの名前を定義
        user_name = session['pokemon_slots'][str(pokemon_index)]
        computer_name = pokemon_list[computer_index].name

        # まだ育てたことがないポケモンなら初期値を保存
        if user_name not in session['pokemon_data']:
            session['pokemon_data'][user_name] = {
                'level': pokemon_list[pokemon_index].level,
                'max_hp': pokemon_list[pokemon_index].max_hp
            }

        if computer_name not in session['computer_data']:
            session['computer_data'][computer_name] = {
                'level': pokemon_list[computer_index].level,
                'max_hp': pokemon_list[computer_index].max_hp
            }

        # 現在HPは最大HPからスタート
        session['user_hp'] = session['pokemon_data'][user_name]['max_hp']
        session['computer_hp'] = session['computer_data'][computer_name]['max_hp']


        return redirect(url_for('battle', pokemon_index=pokemon_index, computer_index=computer_index))

    #選択用リスト
    select_pokemon = []

    for i in range(4):

        pokemon_name = session['pokemon_slots'][str(i)]
        pokemon = pokemon_class_dict[pokemon_name]()
        select_pokemon.append(pokemon)

    return render_template(
        'select.html',
        pokemon_list=select_pokemon
)


#battle(バトルを行う)
@app.route('/battle/<int:pokemon_index>/<int:computer_index>', methods=['GET', 'POST'])
def battle(pokemon_index, computer_index):

    #ポケモンをつくる
    pokemon_name = session['pokemon_slots'][str(pokemon_index)]
    user_pokemon = pokemon_class_dict[pokemon_name]()
    computer_pokemon = pokemon_classes[computer_index]()

    #HPを復元する
    if 'user_hp' in session:
            user_pokemon.hp = session['user_hp']
    if 'computer_hp' in session:
            computer_pokemon.hp = session['computer_hp']

    #actable（行動可能を制御する変数）を復元する
    user_pokemon.actable = session.get('user_actable', 0)
    computer_pokemon.actable = session.get('computer_actable', 0)


    #ポケモンごとのステータス復元
    user_data = session['pokemon_data'][user_pokemon.name]#levelとmax_hpを引っ張ってくる
    computer_data = session['computer_data'][computer_pokemon.name]

    #levelとmax_hpを分ける
    user_pokemon.level = user_data['level']
    user_pokemon.max_hp = user_data['max_hp']

    computer_pokemon.level = computer_data['level']
    computer_pokemon.max_hp = computer_data['max_hp']


    user_message = ""
    computer_message = ""
    evolved = False

    if request.method == 'POST':
        skill_index = int(request.form['skill_index'])
        computer_skill_index = random.randint(0, 3)

        #アタック
        if user_pokemon.hp > 0 :
            if user_pokemon.actable == 0:
                user_message =  user_pokemon.attack(computer_pokemon, skill_index)
            else:
                user_pokemon.actable = 0

        if computer_pokemon.hp > 0:
            if computer_pokemon.actable == 0:
                computer_message = computer_pokemon.attack(user_pokemon, computer_skill_index)
            else:
                computer_pokemon.actable = 0

        #攻撃後にHPを保持する
        session['user_hp'] = user_pokemon.hp
        session['computer_hp'] = computer_pokemon.hp

        #actableを保持する
        session['user_actable'] = user_pokemon.actable
        session['computer_actable'] = computer_pokemon.actable

    if user_pokemon.hp <= 0 or computer_pokemon.hp <= 0:
        #バトル終了時、勝者のステータスを上げる
        if user_pokemon.hp > 0:
            user_pokemon.max_hp += 20
            user_pokemon.level += 1
            user_pokemon.hp = user_pokemon.max_hp

            #進化判定
            old_name = user_pokemon.name
            user_pokemon = user_pokemon.evolve()

            if user_pokemon.name != old_name:

                evolved = True
                
                #進化前のデータを削除
                pokemon_data = session['pokemon_data']
                del pokemon_data[old_name]
            

            #print("===== LEVEL UP =====")
            #print(user_pokemon.name)
            #print("level:", user_pokemon.level)
            #print("max_hp:", user_pokemon.max_hp)


            #更新したステータスを保持する
            pokemon_data = session['pokemon_data']

            pokemon_data[user_pokemon.name] = {
            'level': user_pokemon.level,
            'max_hp': user_pokemon.max_hp
            }

            session['pokemon_data'] = pokemon_data

             # 選択枠を進化後のポケモンに変更
            pokemon_slots = session['pokemon_slots']#復元
            pokemon_slots[str(pokemon_index)] = user_pokemon.name#番号を書き換え
            session['pokemon_slots'] = pokemon_slots#保持

            #print("保存後:")
            #print(session['pokemon_data'])
           

        if computer_pokemon.hp > 0:
            computer_pokemon.max_hp += 20
            computer_pokemon.level += 1
            computer_pokemon.hp = computer_pokemon.max_hp

            computer_data = session['computer_data']

            computer_data[computer_pokemon.name] = {
            'level': computer_pokemon.level,
            'max_hp': computer_pokemon.max_hp
            }

            session['computer_data'] = computer_data

        #hpを保持
        session['user_hp'] = user_pokemon.hp
        session['computer_hp'] = computer_pokemon.hp

        return render_template('result.html', 
                               user_pokemon=user_pokemon, 
                               computer_pokemon=computer_pokemon,
                               user_message=user_message,
                               computer_message=computer_message,
                               evolved=evolved)

    return render_template('battle.html', user_pokemon=user_pokemon,
                           computer_pokemon=computer_pokemon,
                           pokemon_index=pokemon_index,
                           computer_index=computer_index,
                           user_message=user_message,
                           computer_message=computer_message)

#sessinを破棄する（なぜか機能不全。原因不明）
@app.route('/reset')
def reset():
    print("===== RESET =====")
    print(dict(session))
    session.clear()
    session['pokemon_data'] = {
        'ピカチュウ': {'level': 5, 'max_hp': 100},
        'ヒトカゲ': {'level': 5, 'max_hp': 90},
        'ゼニガメ': {'level': 5, 'max_hp': 95},
        'フシギダネ': {'level': 5, 'max_hp': 90},
        'ライチュウ': {'level': 10, 'max_hp': 200}
    }

    session['computer_data'] = {
        'ピカチュウ': {'level': 5, 'max_hp': 100},
        'ヒトカゲ': {'level': 5, 'max_hp': 90},
        'ゼニガメ': {'level': 5, 'max_hp': 95},
        'フシギダネ': {'level': 5, 'max_hp': 90},
        'ライチュウ': {'level': 10, 'max_hp': 200}
    }

    session['pokemon_slots'] = {
        '0': 'ピカチュウ',
        '1': 'ヒトカゲ',
        '2': 'ゼニガメ',
        '3': 'フシギダネ'
    }
    print("===== RESET後 =====")
    print(dict(session))
    return redirect(url_for('index'))
