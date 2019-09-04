<template>
  <div class="hello">
    <img class="border border-info"
      @click="GetImage(thumbnail)"
      v-for="thumbnail in thumbnails"
      :src="'/static/dataset/thumbnail/'+thumbnail"
      :key="thumbnail"
    ></img>
    <button id="fixpolygon" @click="GetFixpolygon">Fixpolygon</button>
    <br>
    <br>
    <label>Response Json: {{msg}}</label>
    <br>
    <br>
    <label>prev_poly array: {{prev_poly_array}}</label>
    <br>
    <br>
    <br>Tool:
    <select id="tool">
      <option value="brush">Brush</option>
      <option value="eraser">Eraser</option>
    </select>
    <div id="container">
      <div
        class="konvajs-content"
        role="presentation"
        style="position: relative; user-select: none; width: 1344px; height: 630px;"
      >
        <canvas
          width="3360"
          height="1575"
          style="padding: 0px; margin: 0px; border: 0px; background: transparent; position: absolute; top: 0px; left: 0px; width: 1344px; height: 630px; display: block;"
        ></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { api } from "../../config/axiosSetting.js";
import Konva from "konva";
const width = window.innerWidth;
const height = window.innerHeight - 25;
var stage = null;
var layer = null;
var context = null;
export default {
  name: "HelloWorld",
  data() {
    return {
      msg: "",
      prev_poly_array: [],
      slot: [],
      configKonva: {
        width: window.innerWidth,
        height: window.innerHeight
      },
      iimage: "",
      thumbnails: [
        "abdomen-ct-01.png",
        "abdomen-ct-02.png",
        "abdomen-ct-03.png"
      ],
      qq:[],
      selectImage:""
    };
  },
  created() {},
  mounted() {
    this.CreateCanvas();
    // this.importThumbnails(
    //   require.context("../assets/dataset/thumbnail/", true, /\.png$/)
    // );
  },
  methods: {
    GetImage(thumbnail) {
      this.iimage = "/static/dataset/image/" + thumbnail;
      this.selectImage = thumbnail;
      this.CreateCanvas();
    },
    async GetFixpolygon() {
      const vm = this;
      var points = [this.slot]
      const params = {
          "propagate_neighbor":100,
          "polygonIndex":0,
          "vertexIndex":this.slot.length,
          "poly":  points,
          "prev_poly": points
      }
      const body = {
        image_path:"/ai-annotated-client-web/static/dataset/image/"+this.selectImage,
        params:JSON.stringify(params)
      };
      console.log(body.poly)
      const res = await api("post", "http://127.0.0.1:5000/fixpolygon", body);
      vm.msg = res;
      const prev_poly = vm.msg;
      vm.prev_poly_array = prev_poly;

      this.Fixpolygon();
    },
    CreateCanvas() {
      const vm = this;
      stage = new Konva.Stage({
        container: "container",
        width: width,
        height: height
      });
      layer = new Konva.Layer();
      stage.add(layer);

      var canvas = document.createElement("canvas");
      canvas.width = stage.width() / 2;
      canvas.height = stage.height() / 2;

      var imageObj = new Image();
      var img = vm.iimage
      imageObj.src = img
      
      var image = new Konva.Image({
        x: stage.width() / 4,
        y: stage.height() / 4,
        width: stage.width() / 2,
        height: stage.height() / 2,
        image: imageObj
      });
     

      var imageCanvas = new Konva.Image({
        image: canvas,
        x: stage.width() / 4,
        y: stage.height() / 4,
        width: stage.width() / 2,
        height: stage.height() / 2,
        stroke: "green",
        shadowBlur: 5
      });
      layer.add(image);
      layer.add(imageCanvas);
      stage.draw();

      context = canvas.getContext("2d");
      context.strokeStyle = "#df4b26";
      context.lineJoin = "round";
      context.lineWidth = 5;

      var isPaint = false;
      var lastPointerPosition;
      var mode = "brush";
      imageCanvas.on("mousedown touchstart", function() {
        isPaint = true;
        lastPointerPosition = stage.getPointerPosition();
      });

      stage.addEventListener("mouseup touchend", function() {
        isPaint = false;
      });

      // and core function - drawing
      stage.addEventListener("mousemove touchmove", function() {
        if (!isPaint) {
          return;
        }

        if (mode === "brush") {
          context.globalCompositeOperation = "source-over";
        }
        if (mode === "eraser") {
          context.globalCompositeOperation = "destination-out";
        }
        context.beginPath();

        var localPos = {
          x: lastPointerPosition.x - image.x(),
          y: lastPointerPosition.y - image.y()
        };
        context.moveTo(localPos.x, localPos.y);
        var pos = stage.getPointerPosition();
        localPos = {
          x: pos.x - image.x(),
          y: pos.y - image.y()
        };
        context.lineTo(localPos.x, localPos.y);
        context.closePath();
        context.stroke();
        lastPointerPosition = pos;
        vm.slot.push([Math.floor(lastPointerPosition.x), Math.floor(lastPointerPosition.y)]);
        layer.batchDraw();
      });

      var select = document.getElementById("tool");
      select.addEventListener("change", function() {
        mode = select.value;
      });
    },
    Fixpolygon() {
      //this.CreateCanvas();
      const vm = this;

      console.log('origin vm.qq:',vm.prev_poly_array) 
      var hihi=[]
      vm.prev_poly_array[0][0].map(c=>{
        c[0] = c[0]+stage.width() / 4
        c[1] = c[1]+stage.height() /4
        console.log("cc :",c)
        hihi.push(c[0]+stage.width() / 4 -1280)
        hihi.push(c[1]+stage.height() /4-750)
      })

      vm.prev_poly_array = vm.prev_poly_array.map(x => x + stage.width() / 4);
      var prePoly=vm.prev_poly_array
      var qqpoly = new Konva.Line({
        points:  hihi,
        fill: "#00D2FF",
        stroke: "black",
        strokeWidth: 5,
        closed: true
      });
      // add the shape to the layer
      layer.add(qqpoly);
      // add the layer to the stage
      stage.add(layer);

      layer.batchDraw();
    }
  }
};
</script>

<style scoped>
</style>
