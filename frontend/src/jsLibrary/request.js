import { apiAddress } from "@/config.js";
import { clearUserInformationCookies } from "@/jsLibrary/cookies.js";

export function sendNormalRequest(
  _this,
  apiUrl,
  content,
  token = false,
  successToastMessage = "",
  returnDataKey = ""
) {
  let axiosConfig = {};
  if (token == true) {
    axiosConfig = {
      headers: { Authorization: `Bearer ${_this.$cookies.get("token")}` },
    };
  }
  _this.$axios
    .post(apiAddress + apiUrl, content, axiosConfig)
    .then((response) => {
      console.log(response.data);
      if (response.data.success == 1) {
        if (successToastMessage != "") {
          _this.$toast.success(successToastMessage, {
            position: "top-center",
            timeout: 2000,
          });
        }
        if (returnDataKey != "") {
          return response.data[returnDataKey];
        }
      } else {
        if (token == true) {
          if (response.data.msg.toLowerCase().includes("token")) {
            clearUserInformationCookies(_this);
            _this.$toast.error(response.data.msg + "\n Please login again", {
              position: "top-center",
              timeout: 2000,
            });
            return;
          }
        }
        _this.$toast.error(response.data.msg, {
          position: "top-center",
          timeout: 2000,
        });
      }
    });
}
