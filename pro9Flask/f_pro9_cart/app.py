from flask import Flask, render_template,render_template_string,request,make_response,redirect, session,url_for
from datetime import timedelta

app=Flask(__name__);

app.secret_key="abcd1234"
app.permanent_session_lifetime=timedelta(minutes=5) #세션 만료시간 5분

products=[
    {"id":1,"name":"노트북","price":350000},
    {"id":2,"name":"물티슈","price":3500},
    {"id":3,"name":"종이컵","price":350},
    {"id":4,"name":"볼펜","price":1500}
]
@app.route("/")
def product_list():
    return render_template("products.html",products=products)

@app.route("/add/<int:product_id>")
def add_to_cart(product_id):
    print("product_id: ",product_id)
    # 세션 cart가 없으면 빈 dict 생성
    cart = session.get("cart",{})

    # next(...., None): 묶음형 자료에서 다음값 1개를 꺼내는 함수
    # 주문상품이 product에 기억됨
    product=next((p for p in products if p["id"]==product_id),None)

    if product is None:
        return "주문 상품을 찾을 수 없다",404

    # 주문 상품이 상품목록에 있으면 장바구니 추가
    item_name=product["name"]
    if item_name in cart:
        cart[item_name]["qty"] +=1 # 카트에 동일 상품이 있는 경우는 수량만 증가
    else:
        cart[item_name]={"price": product["price"], "qty":1}
        # 카트에 최초상품일 경우는 수량1 (qty요소(key) 생성)

    session["cart"]=cart  #변수 cart를 세션 cart키에 값으로 저장
    session.permanent=True
    
    return redirect(url_for("show_cart")) # cart에 저장 후 장바구니(cart 목록) 보기로 이동

@app.route("/cart")
def show_cart(): # 카트의 목록보기
    cart=session.get("cart",{})
    total =sum(info["price"]*info["qty"] for info in cart.values()) # 금액= 단가*수량. 장바구니에 저장된 모든 것
    return render_template("cart.html",cart=cart, total=total)

# 장바구니 부분 삭제
@app.route("/remove/<item_name>") # <item_name> 이거 내 마음대로 줌. 이걸 인자로 넘겨주면됨
def remove_to_cart(item_name): # 여기다가 넘김
    cart=session.get("cart") # <td><a href="/remove/{{name}}">주문 부분삭제</a></td>  <=== cart.html. 형식 없으니 get방식
    # 세션에서 여러개의 key 중 "cart" key값을 모두 읽어 변수에 저장

    if item_name in cart:
        del cart[item_name] #cart 목록에서 부분삭제 상품명을 지움

    session["cart"] = cart # 부분 삭제된 변수 cart를 다시 세션에 cart key에 덩ㅍ어쓰기
    return redirect(url_for("show_cart"))
        

# 장바구니 비우기
@app.route("/clear")
def clear():
    session.pop("cart",None) # 세션의 여러개 키중에서 cart라는 키를 추출(삭제의 효과)
    return redirect(url_for("show_cart"))
# <a href="/clear">모든 주문 삭제(장바구니 비우기)</a> -----> /clear로 끝냄 다른 인자 받을 필요없음
# <td><a href="/remove/{{name}}">주문 부분삭제</a></td> -----> 얘는 name의 인자를 받아야함





if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000);