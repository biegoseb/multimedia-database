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
            <b-row align-v="center" class="my-1">
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
            <b-row align-v="center" class="my-1" v-if="search != 'range'">
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
            <b-row align-v="center" v-if="search == 'range'" class="my-1">
              <b-col md="4" class="p-0">
                Radius:
              </b-col>
              <b-col class="p-0">
                <b-input
                  type="text"
                  pattern="[0-9]+([\.,][0-9]+)?"
                  v-model="radius"
                  placeholder="Query radius"
                ></b-input>
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
    <div class="row" :key="ind" v-for="(persons, ind) in chunkPersons">
      <div class="col-4" :key="index" v-for="(person, index) in persons">
        <v-card width="374" class="my-3">
          <div class="image-upload">
            <label class="cat-photo">
              <b-img class="cat-photo" :src="person[2]"></b-img>
            </label>
          </div>
          <v-card-text class="p-1">
            <b-container class="p-3">
              <b-row align-v="center" class="my-1">
                <b-col md="3" class="p-0">
                  Position:
                </b-col>
                <b-col class="p-0">
                  <b-input :value="calculateIndex(person)"></b-input>
                </b-col>
              </b-row>
              <b-row align-v="center" class="my-1">
                <b-col md="3" class="p-0">
                  Name:
                </b-col>
                <b-col class="p-0">
                  <b-input v-model="person[0]"></b-input>
                </b-col>
              </b-row>
              <b-row align-v="center" class="my-1">
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
    radius: null,
    options: [
      { value: null, text: "Select an option" },
      { value: "sequential", text: "Sequential KNN" },
      { value: "priority", text: "Priority Queue KNN" },
      { value: "range", text: "By Range" },
    ],
  }),
  computed: {
    responseSplit() {
      return this.response.slice(6 * (this.page - 1), 6 * this.page);
    },
    chunkPersons() {
      return this.chunk(this.responseSplit, 3);
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
      if (this.radius != null) {
        data["radius"] = Number(this.radius);
      }
      formData.append("data", JSON.stringify(data));
      axios
        .post("http://127.0.0.1:8082/query", formData, {
          headers: {
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
          this.length = Math.ceil(res.data.length / 6);
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
    chunk(arr, size) {
      return Array.from({ length: Math.ceil(arr.length / size) }, (v, i) =>
        arr.slice(i * size, i * size + size)
      );
    },
    calculateIndex(person) {
      return (
        this.response
          .map((iter) => {
            console.log(iter);
            return iter[2];
          })
          .indexOf(person[2]) + 1
      );
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
  height: 400px;
  width: auto;
}

.cat-photo img {
  object-fit: fill;
}

.theme--light.v-pagination .v-pagination__item--active {
  background-color: #0062cc !important;
}
</style>
