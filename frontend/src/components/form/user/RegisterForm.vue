<template>
  <v-card class="pa-10">
    <div class="ma-5">
      <div class="text-h2 font-weight-thin text-center primary--text dark">
        Register
      </div>
      <div class="my-auto pa-10">
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="inputEmail"
              label="Email"
              :rules="[rules.required, rules.emailFormat, rules.emailLength]"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="inputPassword"
              label="Password"
              :type="showPassword ? 'text' : 'password'"
              :rules="[rules.required, rules.password]"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showPassword = !showPassword"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="checkPassword"
              label="Check Password"
              :type="showCheckPassword ? 'text' : 'password'"
              :rules="[rules.required, rules.password]"
              :append-icon="showCheckPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showCheckPassword = !showCheckPassword"
            ></v-text-field>
          </v-col>
        </v-row>
        <div class="d-flex justify-end">
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="$emit('closeSignInUpInterface')">
            Close
          </v-btn>
          <v-btn color="primary" text @click="login()"> Register </v-btn>
        </div>
        <div class="d-flex justify-end my-5">
          <v-btn color="secondary" text @click="$emit('wantToSignIn')">
            already have acoount?
          </v-btn>
        </div>
      </div>
    </div>
  </v-card>
</template>

<script>
import { rules } from "@/jsLibrary/rules.js";

export default {
  name: "LoginForm",
  data: () => ({
    inputEmail: "",

    inputPassword: "",
    showPassword: false,

    checkPassword: "",
    showCheckPassword: false,

    rules: rules,
  }),
  methods: {
    requestLogin: function () {
      return true;
    },
    login: function () {
      console.log(this.inputEmail, this.inputPassword);
      if (this.requestLogin()) {
        console.log("login success");
      } else {
        console.log("login fail");
      }
    },
  },
};
</script>
