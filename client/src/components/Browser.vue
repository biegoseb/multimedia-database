<template>
  <v-file-input
    v-model="files"
    color="deep-purple accent-4"
    counter
    label="File input"
    multiple
    placeholder="Select your files"
    prepend-icon="mdi-paperclip"
    outlined
    :show-size="1000"
  >
    <template v-slot:selection="{ index, text }">
      <v-chip v-if="index < 2" color="deep-purple accent-4" dark label small>
        {{ text }}
      </v-chip>

      <span
        v-else-if="index === 2"
        class="overline grey--text text--darken-3 mx-2"
      >
        +{{ files.length - 2 }} File(s)
      </span>
    </template>
  </v-file-input>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Browser',
  data: () => ({
    files: [],
  }),
  methods: {
    submitFile() {
        const formData = new FormData()
        formData.append('file', this.file)
        formData.append('k', 1)
        this.progress = true
        axios
          .post('http://127.0.0.1:8082/query', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          .then((res) => {
            console.log('Respuesta local')
            console.log(res)
            console.log(res.data)
            this.urlUpload = res.data
            this.uploadLocalVideo()
          })
          .catch((e) => {
            console.log(e)
          })
      },
      handleFileUpload() {
        this.file = this.$refs.file.files[0]
      },
  }
};
</script>

<style></style>
