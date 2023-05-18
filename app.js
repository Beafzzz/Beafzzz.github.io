let tg = window.Telegram.Webapp;

tg.expand();

tg.MainButton.textColor="#FFFFFF"
tg.MainButton.color="#FFFFFF";

let btn = document.getElementById("btn");

btn.addEventListener("click", function(){
    tg.MainButton.setText("Сообщение отправлено!");
    tg.MainButton.show();
    tg.sendData("Я отправиль")
});