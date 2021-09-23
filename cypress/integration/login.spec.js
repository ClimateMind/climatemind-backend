/// <reference types="cypress" />

import scores from "../fixtures/postScores.json";
var faker = require("faker");

// Expected error responses
const successMessage = "Successfully created user";
const badLoginMessage = "Wrong email or password. Try again.";
const invalidReqMessage =
  "Email, password and recaptcha must be included in the request body.";
const rateLimitPerSecond = "ratelimit exceeded 5 per 1 second";
const rateLimitPerMinute = "ratelimit exceeded 10 per 1 minute";
const rateLimitPerHour = "ratelimit exceeded 50 per 1 hour";
const rateLimitPerDay = "ratelimit exceeded 100 per 1 day";

let session_Id;
let set_one_quizId;
let user;
let user_validCredentials;
let user_invalidCredentials;
let user_invalidEmail;
let user_missingEmail;
let user_missingPassword;
let user_invalidPassword;
let errorMessage;
let recaptcha_Token = "03AGdBq27Tmja4W082LAEVoYyuuALGQwMVxOuOGDduLCQSTWWFuTtc4hQsc-KUVhsJQlBzEjdtxTqs1kXHusJCk2husZjY44rA-opJLWOgJuVUIoGtXozHtYhtmR5DibuJ3idGLalZ00niqnaa0zHC73hWPzc1CtnUO258nZLh1uxePi7DI-afWQd6aa4-EuRcPabG_E500r9S4RReTg42WtP8SNrqEdFoG9UdPoIF2aGCArHD6GqhQzwOev8_jeKUzcxq_1wEvxiID2ow7rxK339PCeTgO9Zz9fPnhTZ6mKaa_tmL1bSQ2zvWvA0Z5An3YvMP3sureZVR_mhJP2r84sYw9WbuI6hRr1oUGtTGuACB-IBqqE5m-meetr870N2Gl-vp3veeEyo34HLj5iDOr6YwyIXWBKam7mDHfhjps1QeiN90291e6CxaFd-bOkeazZyu2_aEPblNwIiUBl0BobqJ2dT2HlxXCRma0QDuX4xLvwh8_ayrJGo9t6nRxQHghZ2ZEh450bM0bVFAqkIGAqYv_EvYj7_XgQ";

describe("'/login' endpoint", () => {
  beforeEach(() => {
    cy.sessionEndpoint().should((response) => {
      session_Id = response.body.sessionId
    }).then(() => {
      cy.scoresEndpoint(scores, session_Id).should((response) => {
        set_one_quizId = response.body.quizId;
      }).then(() => {
        user = {
          firstName: faker.name.firstName(),
          lastName: faker.name.lastName(),
          email: faker.internet.email(),
          password: `@7${faker.internet.password()}`,
          quizId: set_one_quizId
        };
        cy.registerEndpoint(user).should((response) => {
          if (response.status == 201) {
            expect(response.status).to.equal(201);
            expect(response.body.message).to.satisfy(function (s) {
              return s === successMessage;
            });
          } else {
            expect(response.status).to.equal(429);
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            errorMessage = response.body;
            if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
              expect(response.body.error).to.satisfy(function (s) {
                return s === rateLimitPerSecond;
              });
            } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
              expect(response.body.error).to.satisfy(function (s) {
                return s === rateLimitPerMinute;
              });
            } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
              expect(response.body.error).to.satisfy(function (s) {
                return s === rateLimitPerHour;
              });
            }
            else expect(response.body.error).to.satisfy(function (s) {
              return s === rateLimitPerDay;
            });
          }
        });
      });
    });
  });

  it("should log a user in", () => {
    user_validCredentials = {
      "email": user.email,
      "password": user.password,
      "recaptchaToken": recaptcha_Token
    };

    cy.loginEndpoint(user_validCredentials).should((response) => {
      /*expect(response.status).to.equal(200);
      expect(response.headers["content-type"]).to.equal(
        "application/json"
      );
      expect(response.headers["access-control-allow-origin"]).to.equal(
        "http://0.0.0.0:3000"
      );
      expect(response.body).to.be.an("object");
      expect(response.body).to.have.property("message");
      expect(response.body).to.have.property("access_token");
      expect(response.body).to.have.property("user");*/
      expect(response.body.error).to.be.an("object");
      expect(response.body.message).to.satisfy(function (s) {
        return typeof s === "string";
      });
      expect(response.body.access_token).to.satisfy(function (s) {
        return typeof s === "string";
      });
      expect(response.body.user.first_name).to.be.an("string");
      expect(response.body.user.last_name).to.be.an("string");
      expect(response.body.user.email).to.be.an("string");
      expect(response.body.user.user_uuid).to.be.an("string");
      expect(response.body.user.quiz_id).to.be.an("string");
    });
  });

  it("should handle incorrect credentials", () => {
    user_invalidCredentials = {
      email: "invalid@example.com",
      password: "@Invalid1password",
      "recaptchaToken": recaptcha_Token
    };
    cy.loginEndpoint(user_invalidCredentials).should((response) => {
      if (response.status == 401) {
        expect(response.status).to.equal(401);
        expect(response.headers["content-type"]).to.equal(
          "application/json"
        );
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.satisfy(function (s) {
          return s === badLoginMessage;
        });

      } else {
        expect(response.status).to.equal(429);
        expect(response.body).to.have.property("error");
        let errorMessage = response.body;
        if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerSecond;
          });
        } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerMinute;
          });
        } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerHour;
          });
        }
        else expect(response.body.error).to.satisfy(function (s) {
          return s === rateLimitPerDay;
        });
      }
    });
  });

  it("should handle invalid email", () => {
    user_invalidEmail = {
      email: "invalid@example.com",
      password: user.password,
      "recaptchaToken": recaptcha_Token
    };
    cy.loginEndpoint(user_invalidEmail).should((response) => {
      if (response.status == 401) {
        expect(response.status).to.equal(401);
        expect(response.headers["content-type"]).to.equal(
          "application/json"
        );
        expect(response.body).to.be.an("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.satisfy(function (s) {
          return s === badLoginMessage;
        });

      } else {
        expect(response.status).to.equal(429);
        expect(response.body).to.have.property("error");
        let errorMessage = response.body;
        if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerSecond;
          });
        } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerMinute;
          });
        } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerHour;
          });
        }
        else expect(response.body.error).to.satisfy(function (s) {
          return s === rateLimitPerDay;
        });
      }
    });
  });

  it("should handle missing email", () => {
    user_missingEmail = {
      password: user.password,
      "recaptchaToken": recaptcha_Token
    };
    cy.loginEndpoint(user_missingEmail).should((response) => {
      if (response.status == 400) {
        expect(response.status).to.equal(400);
        expect(response.headers["content-type"]).to.equal(
          "application/json"
        );
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.be.a("string");
        expect(response.body.error).to.satisfy(function (s) {
          return s === invalidReqMessage;
        });

      } else {
        expect(response.status).to.equal(429);
        expect(response.body).to.have.property("error");
        let errorMessage = response.body;
        if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerSecond;
          });
        } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerMinute;
          });
        } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerHour;
          });
        }
        else expect(response.body.error).to.satisfy(function (s) {
          return s === rateLimitPerDay;
        });
      }
    });
  });

  it("should handle missing password", () => {
    user_missingPassword = {
      email: user.email,
      "recaptchaToken": recaptcha_Token
    };
    cy.loginEndpoint(user_missingPassword).should((response) => {
      if (response.status == 400) {
        expect(response.status).to.equal(400);
        expect(response.headers["content-type"]).to.equal(
          "application/json"
        );
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.be.a("string");
        expect(response.body.error).to.satisfy(function (s) {
          return s === invalidReqMessage;
        });

      } else {
        expect(response.body.error).to.be.a("string");
        expect(response.status).to.equal(429);
        expect(response.body).to.have.property("error");
        let errorMessage = response.body;
        if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerSecond;
          });
        } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerMinute;
          });
        } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerHour;
          });
        }
        else expect(response.body.error).to.satisfy(function (s) {
          return s === rateLimitPerDay;
        });
      }
    });
  });

  it("should handle invalid password", () => {
    user_invalidPassword = {
      email: user.email,
      password: "@ClimateMind1234!",
      "recaptchaToken": recaptcha_Token
    };
    cy.loginEndpoint(user_invalidPassword).should((response) => {
      if (response.status == 401) {
        expect(response.status).to.equal(401);
        expect(response.headers["content-type"]).to.equal(
          "application/json"
        );
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.be.a("string");
        expect(response.body.error).to.satisfy(function (s) {
          return s === badLoginMessage;
        });

      } else {
        expect(response.status).to.equal(429);
        expect(response.body).to.have.property("error");
        let errorMessage = response.body;
        if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerSecond;
          });
        } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerMinute;
          });
        } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerHour;
          });
        }
        else expect(response.body.error).to.satisfy(function (s) {
          return s === rateLimitPerDay;
        });
      }
    });
  });

  it("should handle missing credentials", () => {
    user_invalidPassword = {
      "recaptchaToken": recaptcha_Token
    };
    cy.loginEndpoint().should((response) => {
      if (response.status == 400) {
        expect(response.status).to.equal(400);
        expect(response.headers["content-type"]).to.equal(
          "application/json"
        );
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.satisfy(function (s) {
          return s === invalidReqMessage;
        });

      } else {
        expect(response.status).to.equal(429);
        expect(response.body).to.have.property("error");
        let errorMessage = response.body;
        if (JSON.stringify(errorMessage).includes("5 per 1 second")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerSecond;
          });
        } else if (JSON.stringify(errorMessage).includes("10 per 1 minute")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerMinute;
          });
        } else if (JSON.stringify(errorMessage).includes("50 per 1 hour")) {
          expect(response.body.error).to.satisfy(function (s) {
            return s === rateLimitPerHour;
          });
        }
        else expect(response.body.error).to.satisfy(function (s) {
          return s === rateLimitPerDay;
        });
      }
    });
  });

  //it.only("should handles too many requests", () => {});
});