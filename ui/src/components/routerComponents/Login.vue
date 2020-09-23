<template>
  <div class="login-wrap layout-wrap">
    <div class="login-layout">
      <div class="login-inner">
        <div class="login-area">
          <h3 class="login-tit">Sign in</h3>
          <div class="input-area">
            <div class="input-wrap">
              <input
                name="userId"
                type="text"
                placeholder="Username"
                class="ip-text"
                v-model="userId"
              />
            </div>
            <div class="input-wrap">
              <input
                name="userPasswd"
                :type="data.isShowPasswd ? 'text' : 'password'"
                placeholder="Password"
                class="ip-text ip-pw"
                v-model="data.userPasswd"
              />
              <span class="btn-show-passwd" @click="showPasswd">
                <img
                  v-if="!!data.isShowPasswd"
                  src="img/icon/icon_passwd_show_off.png"
                />
                <img v-else src="img/icon/icon_passwd_show_on.png" />
              </span>
            </div>
          </div>
          <div class="sign-wrap">
            <div class="submit-button-wrap">
              <a-button
                class="btn-st1"
                size="small"
                type="link"
                @click="onLogin()"
                >login</a-button
              >
              <!-- errorMessage -->
              <div class="error-message-wrap">
                <div
                  class="error-message error-info"
                  v-show="data.errorMessage"
                >
                  {{ data.errorMessage }}
                </div>
              </div>
              <div class="login-set">
                <div class="save-id-box">
                  <input
                    type="checkbox"
                    class="sign-checkbox"
                    id="check-keep"
                    v-model="saveCheck"
                  />
                  <label for="check-keep" class="sign-box" id="checked"></label>
                  <label for="check-keep" class="sign-text"
                    >Keep logged in</label
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
        <!--//로그인 영역-->
      </div>
    </div>
  </div>
</template>
<script>
import { ref, reactive, computed, watch } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { apiUrl, requestRaw, checkAPIResult } from "@/util.js";

// import Loading from "@/components/common/Loading.vue";

export const login = {
  name: "Login",
  setup() {
    const store = useStore();
    const router = useRouter();
    const saveCheck = ref(!!Number(localStorage.getItem("saveCheck")) || 0);
    const userId = ref(localStorage.getItem("saveID") || "");
    const data = reactive({
      userPasswd: "",
      isShowPasswd: false,
      loginResult: "",
      errorMessage: "",
    });
    const getState = computed(() => {
      return store.getters["login/STATE"];
    });

    watch(saveCheck, (value) => {
      value
        ? localStorage.setItem("saveCheck", 1)
        : localStorage.setItem("saveCheck", 0);
      value
        ? localStorage.setItem("saveID", userId.value)
        : localStorage.setItem("saveID", "");
    });

    watch(userId, (value) => {
      saveCheck.value ? localStorage.setItem("saveID", value) : "";
      store.dispatch("login/SET_SAVE_USER", value);
    });

    const showPasswd = () => {
      data.isShowPasswd = !data.isShowPasswd;
    };

    const onLogin = async () => {
      if (Number(localStorage.getItem("saveCheck")) === 1) {
        store.dispatch("login/SET_SAVE_USER", userId.value);
        localStorage.setItem("saveID", userId.value);
      }

      try {
        const params = {
          userId: userId.value,
          userPasswd: data.userPasswd,
        };

        const respObj = checkAPIResult(
          await requestRaw(apiUrl + "Login", params, "post")
        );

        if (respObj) {
          store.dispatch("login/SET_DATA", respObj[0]);
          if (respObj[0].loginResult === 1) {
            router.push({
              name: "content",
            });
          } else {
            data.loginResult = 8;
            data.errorMessage = getState.value.error;
          }
        } else {
          store.dispatch("login/INITIAL_STATE");
          console.log("로그인 서버 에러");
        }
      } catch (err) {
        console.error(err);
        store.dispatch("login/INITIAL_STATE");
      }
    };

    return {
      data,
      saveCheck,
      showPasswd,
      userId,
      onLogin,
      getState,
    };
  },
  // data() {
  //   return {
  //     loginResult: "",
  //     errorMessage: "",
  //     // 버튼 로딩
  //     loader: null,
  //     btLoading: false,
  //   };
  // },
  // watch: {

  //   // 버튼 로딩 처리
  //   loader() {
  //     const l = this.loader;

  //     this[l] = !this[l];

  //     if (l === "stop") {
  //       this["btLoading"] = false;
  //     }

  //     this.loader = null;
  //   },
  // },
  // computed: {
  //   ...mapGetters({
  //     g_loginState: login.STATE,
  //   }),
  // },
  // methods: {
  //   ...mapActions({
  //     a_setLoading: login.SET_LOADING,
  //     a_setLogin: login.SET_DATA,
  //     a_setInitialLogin: login.INITIAL_STATE,
  //     a_setSaveUser: login.SET_SAVE_USER, // 아이디 저장
  //   }),
  //   changeLanguage(lang) {
  //     console.log(lang.short);
  //     this.selectedLanguage = lang.short;
  //   },
  //   //
  //   onSearchText: function (e) {
  //     this.errorMessage = "";
  //     this.loginResult = "";

  //     if (e.keyCode === 13) this.onLogin();
  //   },
  //   // 로그인 버튼
  //   async onLogin() {
  //     this.loader = "btLoading";

  //     if (Number(localStorage.getItem("saveCheck")) === 1) {
  //       const saveUserId = this.userId;
  //       this.a_setSaveUser(saveUserId);
  //       localStorage.setItem("saveID", saveUserId);
  //     }

  //     try {
  //       this.a_setLoading(true);

  //       const params = {
  //         userId: this.userId,
  //         userPasswd: this.userPasswd,
  //       };

  //       const respObj = checkAPIResult(
  //         await requestRaw(apiUrl + "Login", params, "post")
  //       );

  //       if (respObj) {
  //         const data = respObj[0];
  //         // 데이터 초기화
  //         // this.initUser();
  //         this.a_setLogin(data);

  //         if (data.loginResult === 1) {
  //           this.$router.push({
  //             name: "assetInfo",
  //           });

  //           // 로그인 실패 - 횟수 초과
  //         } else if (data.loginResult === 8) {
  //           this.loginResult = 8;
  //           const loginMessageArr = data.loginMessage.split(",");
  //           const remainTime = Number(loginMessageArr[1]);
  //           // 남은 시간
  //           this.timer(loginMessageArr[0], remainTime);

  //           // 로그인 실패
  //         } else {
  //           this.loginResult = data.loginResult;
  //           this.errorMessage = this.g_loginState.error;
  //           if (this.loginResult === 16) {
  //             setTimeout(
  //               () => this.$router.push({ path: "/login/passwdReset" }),
  //               1500
  //             );
  //           }
  //         }
  //       } else {
  //         this.a_setInitialLogin();
  //         console.log("로그인 서버 에러");
  //       }

  //       this.a_setLoading(false);
  //     } catch (err) {
  //       console.error(err);
  //       this.a_setInitialLogin();
  //       this.a_setLoading(false);
  //     }

  //     this.loader = "stop";
  //   },
  //   // 로그인 실패 횟수 초과 - 로그인 제한 남은 시간 카운터
  //   timer(errMsg, seconds) {
  //     const now = Date.now();
  //     const end = now + seconds * 1000;
  //     this.displayTimer(errMsg, seconds);

  //     const intervalTimer = setInterval(() => {
  //       const secondsLeft = Math.round((end - Date.now()) / 1000);

  //       if (secondsLeft === 0) {
  //         this.endTime = 0;
  //       }
  //       if (this.loginResult === 8) {
  //         if (secondsLeft >= 0) {
  //           this.displayTimer(errMsg, secondsLeft);
  //         }
  //       } else {
  //         clearInterval(intervalTimer);
  //         return;
  //       }
  //     }, 1000);
  //   },
  //   displayTimer(errMsg, secondsLeft) {
  //     let minutes = Math.floor((secondsLeft % 3600) / 60);
  //     let seconds = secondsLeft % 60;

  //     // 로그인 제한 시간 있을 경우
  //     if (seconds > 0) {
  //       minutes = minutes < 10 ? "0" + minutes : minutes;
  //       seconds = seconds < 10 ? "0" + seconds : seconds;
  //       this.errorMessage =
  //         errMsg + " (남은 시간: " + minutes + "분 " + seconds + "초" + ")";
  //       // 제한 시간 끝났을 경우
  //     } else {
  //       if (this.loginResult === 8) {
  //         this.errorMessage = "";
  //       }
  //     }
  //   },
  // },
  // components: {
  //   Loading,
  // },
};

export default login;
</script>

<style lang="scss" scoped>
.layout-wrap {
  position: relative;
  display: flex;
  width: 100%;
  height: 100vh;
  font-family: "NanumSquare" !important;
  font-size: 12px;
  font-weight: 400;

  &.login-wrap {
    .login-layout {
      position: relative;
      width: 100%;
      height: 100%;
      background-color: #e1dfef;

      .login-inner {
        position: absolute;
        top: 50%;
        left: 50%;
        width: 570px;
        height: 483px;
        margin-top: -285px;
        margin-left: -285px;
        border-radius: 30px 30px;
        background: #fff;
        box-shadow: 6px 6px 20px 0px #dad8e1;

        .logo {
          position: absolute;
          top: 195px;
          right: 145px;
          justify-content: center;
        }

        .login-area {
          position: absolute;
          top: 90px;
          left: 105px;
          width: 330px;

          &.find-pw-area {
            margin-top: 70px !important;

            .login-tit {
              margin-bottom: 15px;
              font-size: 29px;
            }

            .input-area {
              margin-top: 0;
            }
          }

          .login-tit {
            height: 50px;
            font-size: 35px;
            font-weight: 600;
            letter-spacing: -1px;
            color: #3432a2;
          }

          .login-tit > strong {
            display: inline-block;
            margin: -5px 0 0 9px;
            font-size: 23px;
            font-weight: 400;
            letter-spacing: -0.5px;
            vertical-align: middle;
          }

          .login-tit {
            p {
              line-height: 30px;
              font-size: 14px;
              font-weight: 400;
              color: #c6c6c6;
              letter-spacing: -0.1px;
            }

            .login-tit-p {
              & > p {
                line-height: 20px;
                padding: 6px 0;
                font-size: 13px;
                font-weight: 400;
                color: #c6c6c6;
                letter-spacing: -0.1px;
              }
            }
          }

          /* login input */
          .input-area.box {
            width: 300px;
            margin: 25px 0 0 -10px;
            padding: 20px 29px;
            border-radius: 10px 10px;
            background-color: #fafafa;
          }

          .input-area.box + .btn-wrap {
            margin-top: 22px;
          }

          .input-area.box > .input-wrap {
            height: 20px;
            line-height: 20px;
            margin-bottom: 17px;
          }

          .input-area {
            margin-top: 25px;

            .input-wrap {
              position: relative;
              width: 330px;
              height: 50px;
              line-height: 50px;
              margin-bottom: 10px;
              padding: 0 20px;
              border-radius: 5px 5px;
              background-color: #3432a2 !important;

              &:last-child {
                margin-bottom: 0 !important;
              }

              &.input-pw {
                padding-right: 45px !important;
              }

              .ip-text {
                width: 100%;
                height: 45px;
                border: 0;
                background-color: #3432a2 !important;
                font-size: 13px;
                color: #ffffff;

                &::placeholder {
                  color: rgba(255, 255, 255, 0.5);
                }
              }

              /* 패스워드 보기 잠금 & 해제 */
              .btn-show-passwd {
                position: absolute;
                top: 50%;
                right: 5px;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 40px;
                height: 40px;
                transform: translate(0%, -50%);
                cursor: pointer;
              }
            }

            .input-wrap span {
              font-size: 14px;
              font-weight: 400;
              color: #000;
            }

            .input-wrap > label {
              padding: 0 0 6px 12px;
              font-weight: 400;
            }

            .input-wrap .blk {
              font-size: 13px;
              text-align: left;
            }
          }
        }

        .btn-agent {
          .goto-agent {
            display: flex;
            justify-content: center;
            margin-top: 10px;
            font-size: 13px;
            color: #8681b6;
          }

          .goto-agent:hover {
            color: #c6c6c6;
          }
        }
      }
    }

    .find-result-box {
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      height: 45px;
      line-height: 45px;
      border: 0;
      border-radius: 5px 5px;
      background-color: #3432a2;
      font-size: 13px;
      color: #ffffff;
    }
  }
}

/* button */
.sign-wrap {
  position: relative;

  .error-message-wrap {
    height: 17px;
    line-height: 17px;
    margin-top: 5px;

    .error-message {
      transition: all 0.3s;

      &.error-info {
        display: block;
        width: 100%;
        padding-left: 6px;
        font-size: 12px;
        font-weight: 500;
        color: red;
        text-align: center;
        letter-spacing: 0;
      }

      &.success {
        color: #c6c6c6 !important;
      }
    }
  }

  .submit-button-wrap {
    margin-top: 10px;

    .button {
      width: 45px;
      height: 20px;
      border-radius: 5px 5px;
      font-size: 14px;
      cursor: pointer;

      &.a-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
      }
    }

    .btn-st1 {
      background-color: #0f046d !important;
      font-weight: normal;
      color: #ffffff !important;
      border-radius: 5px 5px;
      text-transform: none;
      font-size: 14px;
    }

    .btn-st2 {
      height: 20px;
      color: #8b81b6;
      border-bottom: 1px solid #8b81b6;
      text-decoration: none;
      letter-spacing: -0.3px;

      &:hover {
        color: #c6c6c6;
      }
    }
    .btn-st3 {
      background-color: transparent;
      color: #8b81b6;
      margin-top: 10px;
      margin-left: 116px;
      font-size: 13px;

      &:hover {
        color: #c6c6c6;
        background-color: transparent !important;
      }
    }

    .login-set {
      display: flex;
      justify-content: space-between;
      margin-top: 5px;
    }

    // 아이디 저장
    .save-id-box {
      display: flex;
      align-items: center;
      margin: 0 0 10px 6px;

      .sign-checkbox {
        display: none;
      }

      .sign-box {
        position: relative;
        display: block;
        width: 18px;
        height: 18px;
        margin: 0;
        // border: 1px solid #cecece;
        border-radius: 3px;
        background-color: #3432a3;
        box-sizing: border-box;
        cursor: pointer;

        &:hover {
          border-color: #ffffff;
        }

        &::before {
          content: "";
          position: absolute;
          top: 50%;
          left: 50%;
          display: block;
          width: 13px;
          height: 9px;
          opacity: 0;
        }
      }

      .sign-text {
        line-height: 18px;
        margin: 0 0 0 4px !important;
        font-size: 13px;
        color: #8b81b6;
        letter-spacing: -0.1px;
        cursor: pointer;

        &:hover {
          color: #c6c6c6;
        }
      }

      .sign-checkbox:checked + .sign-box {
        border-color: #ffffff;
        background-image: url("/img/icon/icon_check.png");
        background-repeat: no-repeat;
        background-color: #3432a3;
        background-position: 50%;
      }

      .sign-checkbox:checked + .sign-box + .sign-text {
        color: #3432a3;
      }
    }
  }
}

input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
  transition: background-color 5000s ease-in-out 0s;
  -webkit-transition: background-color 9999s ease-out;
  -webkit-box-shadow: 0 0 0px 1000px #3432a2 inset !important;
  -webkit-text-fill-color: #fff !important;
}
</style>
