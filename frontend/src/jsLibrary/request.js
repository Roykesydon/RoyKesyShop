import { apiAddress } from "@/config.js";
import { clearUserInformationCookies } from "@/jsLibrary/cookies.js";

export function sendNormalRequest(
  _this,
  method,
  apiUrl,
  data,
  params,
  token = false,
  successToastMessage = "",
  returnDataKey = ""
) {
  return new Promise((resolve, reject) => {
    let axiosRequest = {
      method: method,
      url: apiAddress + apiUrl,
      data: data,
      params: params,
    };
    if (token == true) {
      axiosRequest["headers"] = {
        Authorization: `Bearer ${_this.$cookies.get("token")}`,
      };
    }

    _this.$axios(axiosRequest).then((response) => {
      console.log(response.data);
      if (response.data.success == 1) {
        if (successToastMessage != "") {
          _this.$toast.success(successToastMessage, {
            position: "top-center",
            timeout: 2000,
          });
        }
        if (returnDataKey != "") {
          resolve(response.data[returnDataKey]);
        }
        resolve();
      } else {
        if (token == true) {
          if (response.data.msg.toLowerCase().includes("token")) {
            clearUserInformationCookies(_this);
            _this.$toast.error(response.data.msg + "\n Please login again", {
              position: "top-center",
              timeout: 2000,
            });
            resolve("success");
          }
        }
        _this.$toast.error(response.data.msg, {
          position: "top-center",
          timeout: 2000,
        });
        reject("error");
      }
    });
  });
}
