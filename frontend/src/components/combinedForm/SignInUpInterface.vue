<template>
  <div>
    <v-card>
      <div v-if="wantLogin">
        <login-form
          @closeSignInUpInterface="$emit('closeSignInUpInterface')"
          @wantToSignUp="wantLogin = false"
        />
      </div>
      <div v-else>
        <register-form
          style="min-height: 55vh"
          @closeSignInUpInterface="$emit('closeSignInUpInterface')"
          @wantToSignIn="wantLogin = true"
        />
      </div>
    </v-card>
  </div>
</template>

<script>
import LoginForm from "@/components/form/user/LoginForm.vue";
import RegisterForm from "@/components/form/user/RegisterForm.vue";

export default {
  name: "SignInUpInterface",
  components: { LoginForm, RegisterForm },
  data: () => ({ wantLogin: true }),
};
</script>

<style>
.v-window__container {
  height: 50vh;
}
</style>
