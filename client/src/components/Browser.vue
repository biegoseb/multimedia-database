<template>
  <div class="container">
    <div class="row">
      <v-card width="374" key="photo" class="mx-auto m-2">
        <div class="image-upload">
          <label for="photo" class="cat-photo">
            <b-img
              class="cat-photo"
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
          <b-container class="p-3">
            <b-row align-v="center">
              <b-col md="3" class="p-0">
                Nombre:
              </b-col>
              <b-col class="p-0">
                <b-input v-model="nombre"></b-input>
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col md="3" class="p-0">
                Number K:
              </b-col>
              <b-col class="p-0">
                <b-input v-model="k"></b-input>
              </b-col>
            </b-row>
          </b-container>
        </v-card-text>
      </v-card>
    </div>
    <div class="row justify-content-end">
      <button class="btn btn-primary" @click="submitFile()">Submit</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Browser",
  data: () => ({
    nombre: "",
    k: "",
    src: "",
    files: [],
    photoPlaceholder: require("../static/img/38.jpg"),
  }),
  methods: {
    submitFile() {
      const formData = new FormData();
      formData.append("file", this.files);
      const data = {
        k: Number(this.k),
        nombre: this.nombre,
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
.image-upload > input {
  display: none;
}

.image-upload img {
  max-width: 100%;
  cursor: pointer;
}

.cat-photo {
  height: 40vh;
  width: 40vh;
}
.cat-photo img {
  object-fit: fill;
}
</style>
