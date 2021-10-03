// /// <reference types="cypress" />

import scores from "../fixtures/postScores.json"

var faker = require("faker");

let session_Id;
let set_one_quizId;
let user1;
let user2;
let accessToken;
let updateEmailBody;
let newEmail;
let confirmNewEmail;
let user1_oldEmail;
let errorMessage;

const successMessage = "Successfully created user";
const successEmailUpdateMessage = "User email successfully updated.";
const invalidEmailFormatMessage = "Cannot update email. Email is not formatted correctly.";
const notMatchMessage = "Cannot update email. New email address and confirm new email address do not match.";
const missingNewEmailMessage = "newEmail must be included in the request body.";
const missingConfirmNewEmailMessage = "confirmEmail must be included in the request body.";
const missingPasswordMessage = "password must be included in the request body.";
const invalidPasswordMessage = "Cannot update email. Incorrect password.";
const emailAlreadyExistsInDBMessage = "Cannot update email. Email already exists in the database."
const badLoginMessage = "Wrong email or password. Try again.";
const successfulLoginMessage = "successfully logged in user";
const MissingJWTMessage = 'Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie "access_token")'
const expiredAccessToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjMwNDcyOTUzLCJqdGkiOiIyZTMzZThjNy1iNTQyLTQ5MmQtYjVkMS0xNmU4NWFlZjlhYzIiLCJuYmYiOjE2MzA0NzI5NTMsInR5cGUiOiJhY2Nlc3MiLCJzdWIiOiI1RDZFNjM0MS1CRjJBLTRGM0ItOTBCOS04NzA5NTUwN0YxOEYiLCJleHAiOjE2MzA0NzM4NTN9.osRQqeVJJaHitPtBmjB2mjwY3PIhgnEzX5Z4-fLzlBc";
const expiredAccessTokenMessage = "Token has expired";
const rateLimitPerSecond = "ratelimit exceeded 5 per 1 second";
const rateLimitPerMinute = "ratelimit exceeded 10 per 1 minute";
const rateLimitPerHour = "ratelimit exceeded 50 per 1 hour";
const rateLimitPerDay = "ratelimit exceeded 100 per 1 day";
let recaptcha_Token = "03AGdBq27Tmja4W082LAEVoYyuuALGQwMVxOuOGDduLCQSTWWFuTtc4hQsc-KUVhsJQlBzEjdtxTqs1kXHusJCk2husZjY44rA-opJLWOgJuVUIoGtXozHtYhtmR5DibuJ3idGLalZ00niqnaa0zHC73hWPzc1CtnUO258nZLh1uxePi7DI-afWQd6aa4-EuRcPabG_E500r9S4RReTg42WtP8SNrqEdFoG9UdPoIF2aGCArHD6GqhQzwOev8_jeKUzcxq_1wEvxiID2ow7rxK339PCeTgO9Zz9fPnhTZ6mKaa_tmL1bSQ2zvWvA0Z5An3YvMP3sureZVR_mhJP2r84sYw9WbuI6hRr1oUGtTGuACB-IBqqE5m-meetr870N2Gl-vp3veeEyo34HLj5iDOr6YwyIXWBKam7mDHfhjps1QeiN90291e6CxaFd-bOkeazZyu2_aEPblNwIiUBl0BobqJ2dT2HlxXCRma0QDuX4xLvwh8_ayrJGo9t6nRxQHghZ2ZEh450bM0bVFAqkIGAqYv_EvYj7_XgQ";

describe("'/email' endpoint", () => {
    describe("logged in user Udating their email", () => {
        before(() => {
            cy.sessionEndpoint().should((response) => {
                session_Id = response.body.sessionId
            }).then(() => {
                cy.scoresEndpoint(scores, session_Id).should((response) => {
                    set_one_quizId = response.body.quizId;
                }).then(() => {
                    user1 = {
                        "firstName": faker.name.firstName(),
                        "lastName": faker.name.lastName(),
                        "email": faker.internet.email(),
                        "password": `@7${faker.internet.password()}`,
                        "quizId": set_one_quizId
                    };

                    cy.registerEndpoint(user1).should((response) => {
                        if (response.status == 201) {
                            expect(response.status).to.equal(201);
                            expect(response.body.message).to.satisfy(function (s) {
                                return s === successMessage;
                            });
                            accessToken = response.body.access_token;
                        } else {
                            expect(response.status).to.equal(429);
                            expect(response.body).to.have.property("error");
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

        it("should get current email", () => {
            cy.emailEndpoint(accessToken)
                .should((response) => {
                    expect(response.status).to.equal(200);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.headers["access-control-allow-origin"]).to.equal("*");
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("currentEmail");
                    expect(response.body.currentEmail).to.be.a("string");
                    expect(response.body.currentEmail).to.satisfy(function (s) {
                        return s === user1.email;
                    });
                });
        });

        it("should update current email", () => {
            newEmail = faker.internet.email();
            confirmNewEmail = newEmail;

            updateEmailBody = {
                "newEmail": newEmail,
                "confirmEmail": confirmNewEmail,
                "password": user1.password
            };

            cy.updateEmailEndpoint(accessToken, updateEmailBody)
                .should((response) => {
                    expect(response.status).to.equal(200);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.headers["access-control-allow-origin"]).to.equal("*");
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("message");
                    expect(response.body.message).to.be.a("string");
                    expect(response.body.message).to.satisfy(function (s) {
                        return s === successEmailUpdateMessage;
                    });
                });
        });

        it("should log a user in with an updated email", () => {
            newEmail = faker.internet.email();
            confirmNewEmail = newEmail;

            updateEmailBody = {
                "newEmail": newEmail,
                "confirmEmail": confirmNewEmail,
                "password": user1.password
            };

            cy.updateEmailEndpoint(accessToken, updateEmailBody)
                .should((response) => {
                    expect(response.status).to.equal(200);
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("message");
                    expect(response.body.message).to.be.a("string");
                    expect(response.body.message).to.satisfy(function (s) {
                        return s === successEmailUpdateMessage;
                    });
                });
            
            //Login with an updated email
            let user_updatedEmail = {
                "email": updateEmailBody.newEmail,
                "password": updateEmailBody.password,
                "recaptchaToken": recaptcha_Token
            };

            cy.loginEndpoint(user_updatedEmail).should((response) => {
                expect(response.body.message).to.be.a("string")
                expect(response.status).to.equal(200);
                expect(response.body.message).to.satisfy(function (s) {
                    return s === successfulLoginMessage;
                });
            });
        });

        it("should not log a user in with an old email", () => {
            newEmail = faker.internet.email();
            confirmNewEmail = newEmail;

            updateEmailBody = {
                "newEmail": newEmail,
                "confirmEmail": confirmNewEmail,
                "password": user1.password
            };

            cy.updateEmailEndpoint(accessToken, updateEmailBody)
                .should((response) => {
                    expect(response.status).to.equal(200);
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("message");
                    expect(response.body.message).to.be.a("string");
                    expect(response.body.message).to.satisfy(function (s) {
                        return s === successEmailUpdateMessage;
                    });
                });
            
            //Login with old email
            user1_oldEmail = {
                "email": user1.email,
                "password": user1.password,
                "recaptchaToken": recaptcha_Token
            };

            cy.loginEndpoint(user1_oldEmail).should((response) => {
                expect(response.status).to.equal(401);
                expect(response.body).to.be.an("object");
                expect(response.body).to.have.property("error");
                expect(response.body.error).to.be.a("string");
                expect(response.body.error).to.satisfy(function (s) {
                    return s === badLoginMessage;
                });
            });
        });

        it("should handle invalid email format when updating current email", () => {
            newEmail = faker.lorem.word();
            confirmNewEmail = newEmail;

            updateEmailBody = {
                "newEmail": newEmail,
                "confirmEmail": confirmNewEmail,
                "password": user1.password
            };
            
            cy.updateEmailEndpoint(accessToken, updateEmailBody)
                .should((response) => {
                    expect(response.status).to.equal(400);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.headers["access-control-allow-origin"]).to.equal("*");
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("error");
                    expect(response.body.error).to.be.a("string");
                    expect(response.body.error).to.satisfy(function (s) {
                        return s === invalidEmailFormatMessage;
                    });
                });
        });

        it("should handle new email address and confirm new email address that do not match", () => {
            newEmail = faker.internet.email();
            confirmNewEmail = faker.internet.email();
            
            updateEmailBody = {
                "newEmail": newEmail,
                "confirmEmail": confirmNewEmail,
                "password": user1.password
            };
            
            cy.updateEmailEndpoint(accessToken, updateEmailBody)
                .should((response) => {
                    expect(response.status).to.equal(400);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.headers["access-control-allow-origin"]).to.equal("*");
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("error");
                    expect(response.body.error).to.be.a("string");
                    expect(response.body.error).to.satisfy(function (s) {
                        return s === notMatchMessage;
                    });
                });
        });

        it("should handle updating email without newEmail", () => {
            newEmail = faker.internet.email();
            confirmNewEmail = newEmail;
            
            updateEmailBody = {
                "confirmEmail": confirmNewEmail,
                "password": user1.password
            };
            
            cy.updateEmailEndpoint(accessToken, updateEmailBody)
                .should((response) => {
                    expect(response.status).to.equal(400);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.headers["access-control-allow-origin"]).to.equal("*");
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("error");
                    expect(response.body.error).to.be.a("string");
                    expect(response.body.error).to.satisfy(function (s) {
                        return s === missingNewEmailMessage;
                    });
                });
        });

        it("should handle updating email without confirmEmail", () => {
            newEmail = faker.internet.email();
            
            updateEmailBody = {
                "newEmail": newEmail,
                "password": user1.password
            };
            
            cy.updateEmailEndpoint(accessToken, updateEmailBody)
                .should((response) => {
                    expect(response.status).to.equal(400);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.headers["access-control-allow-origin"]).to.equal("*");
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("error");
                    expect(response.body.error).to.be.a("string");
                    expect(response.body.error).to.satisfy(function (s) {
                        return s === missingConfirmNewEmailMessage;
                    });
                });
        });

        it("should handle updating email without password", () => {
            newEmail = faker.internet.email();
            confirmNewEmail = newEmail;
            
            updateEmailBody = {
                "newEmail": newEmail,
                "confirmEmail": confirmNewEmail
            };
            
            cy.updateEmailEndpoint(accessToken, updateEmailBody)
                .should((response) => {
                    expect(response.status).to.equal(400);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.headers["access-control-allow-origin"]).to.equal("*");
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("error");
                    expect(response.body.error).to.be.a("string");
                    expect(response.body.error).to.satisfy(function (s) {
                        return s === missingPasswordMessage;
                    });
                });
        });

        it("should handle updating email using invalid password", () => {
            newEmail = faker.internet.email();
            confirmNewEmail = newEmail;
            
            updateEmailBody = {
                "newEmail": newEmail,
                "confirmEmail": confirmNewEmail,
                "password": faker.internet.password()
            };
            
            cy.updateEmailEndpoint(accessToken, updateEmailBody)
                .should((response) => {
                    expect(response.status).to.equal(401);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.headers["access-control-allow-origin"]).to.equal("*");
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("error");
                    expect(response.body.error).to.be.a("string");
                    expect(response.body.error).to.satisfy(function (s) {
                        return s === invalidPasswordMessage;
                    });
                });
        });

    });

    describe("unlogged in user trying to update their email", () => {
        it("should handle trying to get current email without an access_token", () => {
            cy.request({
                method: 'GET',
                url: 'http://localhost:5000/email',
                failOnStatusCode: false,
            })
            .should((response) => {
                    expect(response.status).to.equal(401);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("msg");
                    expect(response.body.msg).to.be.a("string");
                    expect(response.body.msg).to.satisfy(function (s) {
                        return s === MissingJWTMessage;
                    });
                });
        });

        it("should handle updating email without an access_token", () => {
            cy.request({
                    method: 'PUT',
                    url: 'http://localhost:5000/email',
                    failOnStatusCode: false,
                })
                .should((response) => {
                    expect(response.status).to.equal(401);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("msg");
                    expect(response.body.msg).to.be.a("string");
                    expect(response.body.msg).to.satisfy(function (s) {
                        return s === MissingJWTMessage;
                    });
                });
        });
    });

    describe("Updating email with an Expired Token", () => {
        it("should handle trying to get current email with an Expired Token", () => {
            cy.emailEndpoint(expiredAccessToken)
                .should((response) => {
                    expect(response.status).to.equal(401);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("msg");
                    expect(response.body.msg).to.be.a("string");
                    expect(response.body.msg).to.satisfy(function (s) {
                        return s === expiredAccessTokenMessage;
                    });
                });
        });

        it("should handle updating email with an Expired Token", () => {
            cy.updateEmailEndpoint(expiredAccessToken)
                .should((response) => {
                    expect(response.status).to.equal(401);
                    expect(response.headers["content-type"]).to.equal("application/json");
                    expect(response.body).to.be.an("object");
                    expect(response.body).to.have.property("msg");
                    expect(response.body.msg).to.be.a("string");
                    expect(response.body.msg).to.satisfy(function (s) {
                        return s === expiredAccessTokenMessage;
                    });
                });
        });
    });
});
