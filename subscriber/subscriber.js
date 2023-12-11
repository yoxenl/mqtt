let mqttClient;
let json;

window.addEventListener("load", (event) => {
  connectToBroker();

  const onBTN = document.querySelector('#ON');
  onBTN.addEventListener("click", function () {
    OnButton();
  });

  const offBTN = document.querySelector('#OFF');
  offBTN.addEventListener("click", function () {
    OffButton();
  });

});

const systemfailurebutton = document.querySelector(".dot");
const OffBtn = document.getElementById("OFF");
const ONBtn = document.getElementById("ON");
const clientId = Math.floor(Math.random() * 1000)
const messageTextAreaMaxSpeed = document.querySelector("#max_Speed_Message");
const messageTextArea = document.querySelector("#speed_Message");
messageTextArea.value = 0;

function connectToBroker() {

  // Change this to point to your MQTT broker
  //const host = "ws://broker.emqx.io:8083/mqtt";
  const host = "ws://10.0.20.114:9001/mqtt";
  const options = {
    keepalive: 60,
    clientId: clientId,
    protocolId: "MQTT",
    protocolVersion: 5,
    clean: true,
    reconnectPeriod: 1000,
    connectTimeout: 30 * 1000,
  };

  mqttClient = mqtt.connect(host, options);
  mqttClient.subscribe("andel1", { qos: 0 });

  mqttClient.on("error", (err) => {
    console.log("Error: ", err);
    mqttClient.end();
  });

  mqttClient.on("reconnect", () => {
    console.log("Reconnecting...");
  });

  mqttClient.on("connect", () => {
    console.log("Client connected:" + clientId);
  });

  // Received
  mqttClient.on("message", (topic, message, packet) => {
    const obj = JSON.parse(message.toString());
    console.log(obj);

    if(obj.Type == clientId){
      if(obj.hasOwnProperty("Off")){
        if(obj.Off){
              OffBtn.classList.add("active");
              ONBtn.classList.remove("active");
              messageTextAreaMaxSpeed.value = 0 + "\r\n";
        } else {
            ONBtn.classList.add("active");
            OffBtn.classList.remove("active");
          }
      }
    
      if(obj.Failure){
        ONBtn.classList.remove("active");
        OffBtn.classList.add("active");
        systemfailurebutton.style.background = "red";
        messageTextAreaMaxSpeed.value = 0;
      }
      if(!obj.Failure){
        systemfailurebutton.style.background = "grey";
      }
      console.log("hastigheten är " + parseInt(obj.Speed));
      console.log("hastigheten som skickades är en siffra: " + isNaN(parseInt(obj.Speed)));
      if(!isNaN(parseInt(obj.Speed)) && ONBtn.classList.contains("active")){
        messageTextAreaMaxSpeed.value = obj.Speed + "\r\n";
      }
    }  
  });
}

function OnButton(){
  if(systemfailurebutton.style.background == "red"){
    return
  }
  console.log("button pressed ON");
  ONBtn.classList.add("active");
  OffBtn.classList.remove("active");
}

function OffButton(){
  console.log("button pressed OFF");
  OffBtn.classList.add("active");
  ONBtn.classList.remove("active");
  messageTextAreaMaxSpeed.value = 0 + "\r\n";
}


function whatsTheSpeed(){
  console.log("SENDING NEW SPEED" + " THE ID IS " + clientId);
  var speed = Math.floor(Math.random() * ((10-1)+1)+ 1);
  var status;
  if(ONBtn.classList.contains("active")){
    status = "ON";
  } else {
    status = "OFF";
  }
  if(speed > getMaxSpeed())
    speed = getMaxSpeed();
  var robot = {
    Robot : clientId,
    Speed : speed,
    Time : new Date().getTime(),
    MaxSpeed : getMaxSpeed(),
    Status : status,
  }

  mqttClient.publish("andel1337", JSON.stringify(robot), {
    qos: 0,
    retain: false,
  });

  
  mqttClient.publish("andel420", JSON.stringify(robot), {
    qos: 0,
    retain: false,
  });

  messageTextArea.value = speed + "\r\n";

}


setInterval(function(){
  whatsTheSpeed()
},1000)

function getMaxSpeed(){
  return Number(messageTextAreaMaxSpeed.value);
}