<template>
  <div class="container">
    <div class="row">
      <v-card width="374" key="photo" class="mx-auto m-2">
        <div class="image-upload">
          <label for="photo" class="cat-photo">
            <b-img
              class="cat-photo"
              fluid
              :src="src === '' ? photoPlaceholder : src"
            ></b-img>
          </label>
          <input
            id="photo"
            ref="inputFile"
            accept="image/*"
            type="file"
            @change="onFileChange($event)"
          />
        </div>
        <v-card-text class="p-1">
          <b-container class="px-4 py-2">
            <b-row align-v="center">
              <b-col md="4" class="p-0">
                K results:
              </b-col>
              <b-col class="p-0">
                <b-input
                  min="1"
                  type="number"
                  v-model="k"
                  placeholder="Number of k results"
                ></b-input>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col md="4" class="p-0">
                Type of Search:
              </b-col>
              <b-col class="p-0">
                <b-form-select
                  v-model="search"
                  :options="options"
                ></b-form-select>
              </b-col>
            </b-row>
            <div class="row justify-content-center mt-4">
              <button class="btn btn-primary" @click="submitFile()">
                Submit
              </button>
            </div>
          </b-container>
        </v-card-text>
      </v-card>
    </div>
    <br />
    <div
      class="row justify-content-around"
      style="color: #2d2d2d; font-family: 'Teko', sans-serif; font-size:2rem;"
    >
      <div>
        Results:
      </div>
      <div class="text-center">
        <v-pagination
          v-model="page"
          :length="length"
          :total-visible="total"
        ></v-pagination>
      </div>
    </div>
    <div class="row">
      <v-card
        :key="index"
        width="374"
        class="my-2"
        v-for="(person, index) in responseSplit"
      >
        <div class="image-upload">
          <label class="cat-photo">
            <b-img class="cat-photo" :src="person[2]"></b-img>
          </label>
        </div>
        <v-card-text class="p-1">
          <b-container class="p-3">
            <b-row align-v="center">
              <b-col md="3" class="p-0">
                Name:
              </b-col>
              <b-col class="p-0">
                <b-input v-model="person[0]"></b-input>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col md="3" class="p-0">
                Distance:
              </b-col>
              <b-col class="p-0">
                <b-input v-model="person[1]"></b-input>
              </b-col>
            </b-row>
          </b-container>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Browser",
  data: () => ({
    k: "",
    src: "",
    files: [],
    photoPlaceholder: require("../static/img/camera.jpg"),
    response: [],
    page: 1,
    length: 1,
    total: 7,
    search: null,
    options: [
      { value: null, text: "Select an option" },
      { value: "sequential", text: "Sequential KNN" },
      { value: "priority", text: "Priority Queue KNN" },
    ],
  }),
  computed: {
    responseSplit() {
      return this.response.slice(7 * (this.page - 1), 6 * this.page);
    },
  },
  methods: {
    submitFile() {
      const formData = new FormData();
      formData.append("file", this.files);
      const data = {
        k: this.k == "" ? 1 : Number(this.k),
        search: this.search == "" ? "priority" : this.search,
      };
      formData.append("data", JSON.stringify(data));
      axios
        .post("http://127.0.0.1:8082/query", formData, {
          headers: {
            /* "Content-Type": "multipart/form-data", */
            "Content-Type": false,
            processData: false,
          },
        })
        .then((res) => {
          console.log("Respuesta local");
          console.log(res);
          this.response = res.data;
          for (let i = 0; i < res.data.length; i++) {
            this.response[i][2] = require("../../../server/data/" +
              this.response[i][2]);
          }
          this.length = res.data.length / 6;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    handleFileUpload() {
      this.file = this.$refs.file.files[0];
    },
    onFileChange(e) {
      const file = e.target.files[0];
      this.files = e.target.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        this.src = e.target.result;
      };
      reader.readAsDataURL(file);
    },
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Teko:wght@500&display=swap");
.image-upload > input {
  display: none;
}

.image-upload img {
  max-width: 100%;
  cursor: pointer;
}

.cat-photo {
  /* height: 40vh;
  width: 40.2vw; */
  height: 400px;
  width: 375px;
}
.cat-photo img {
  object-fit: fill;
}
</style>
