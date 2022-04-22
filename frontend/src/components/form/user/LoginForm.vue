<template>
  <v-card class="pa-10">
    <div class="ma-5">
      <div class="text-h2 font-weight-thin text-center primary--text dark">
        Login
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
        </v-row>
        <div class="d-flex justify-end">
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="$emit('closeSignInUpInterface')">
            Close
          </v-btn>
          <v-btn color="primary" text @click="login()"> Login </v-btn>
        </div>
        <div class="d-flex justify-end my-5">
          <v-btn color="secondary" text @click="$emit('wantToSignUp')">
            don't have acoount?
          </v-btn>
        </div>
      </div>
    </div>
  </v-card>
</template>

<script>
import { rules } from "@/jsLibrary/rules.js";
import { loginErrorMessage } from "@/assets/errorMessage/English/user/loginError.js";

export default {
  name: "LoginForm",
  data: () => ({
    inputEmail: "",

    inputPassword: "",
    showPassword: false,

    rules: rules,
  }),
  methods: {
    requestLogin: function () {
      return 1;
    },
    login: function () {
      console.log(this.inputEmail, this.inputPassword);
      let errorMessageCode = this.requestLogin();
      if (errorMessageCode == 0) {
        this.$toast.success("Login Success", {
          position: "top",
        });
      } else {
        this.$toast.error(loginErrorMessage[errorMessageCode], {
          position: "top",
        });
      }
    },
  },
};
</script>
