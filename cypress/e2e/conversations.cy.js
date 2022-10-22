//  /// <reference types="cypress" />
import scores from "../fixtures/postScores.json";

var faker = require("faker");

let session_Id;
let set_one_quizId;
let user;
let accessToken;
const invalidInvitedUsername = "Must provide a name that is up to 20 characters long.";
const missingJSONBodyMessage = "Must provide a JSON body with the name of the invited user.";
const SESSION_UUIDNotInDBMessage = "SESSION_UUID is not in the db.";
const uuidFormatChecker_LowerCase = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/;
const uuidFormatChecker_UpperCase = /[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}/;
const createdSuccessfulMessage = "conversation created";
let requestBody;
let invitedUserName;

describe("'/conversation' endpoint", () => {
    beforeEach(() => {
        cy.sessionEndpoint().should((response) => {
            session_Id = response.body.sessionId
        }).then(() => {
            cy.scoresEndpoint(scores, session_Id).should((response) => {
                set_one_quizId = response.body.quizId;
            }).then(() => {
                user = {
                    "firstName": faker.name.firstName(),
                    "lastName": faker.name.lastName(),
                    "email": faker.internet.email(),
                    "password": `@7${faker.internet.password()}`,
                    "quizId": set_one_quizId
                };
                expect(user.firstName).to.be.a('string')
                cy.registerEndpoint(user).should((response) => {
                    expect(response.status).to.equal(201);
                    accessToken = response.body.access_token;
                    expect(response.body.access_token).to.be.a('string')
                });
            });
        });
    });

    it("should create a conversation", () => {
        //Generate a username to be invited
        requestBody = {
            "invitedUserName": faker.name.firstName()
        };
        expect(requestBody).to.be.an("object");
        expect(requestBody.invitedUserName).to.be.a("string");

        //Create a conversation and test the response body
        cy.conversationEndpoint(requestBody, accessToken, session_Id).should((response) => {
            expect(response.status).to.equal(201);
            expect(response.headers["content-type"]).to.equal(
                "application/json"
            );
            expect(response.body).to.be.an("object");
            expect(response.body).to.have.property("message");
            expect(response.body).to.have.property("conversationId");
            expect(response.body.message).to.be.a("string");
            expect(response.body.message).to.deep.equal(createdSuccessfulMessage);
            expect(response.body.conversationId).to.be.a("string");
            expect(response.body.conversationId).to.match(uuidFormatChecker_LowerCase);
        });
    });

    it("should get conversations", () => {
        //Create many conversation
        let i = 0;
        while (i < 3) {
            //Generate a username to be invited
            requestBody = {
                "invitedUserName": faker.name.firstName()
            };
            expect(requestBody).to.be.an("object");
            expect(requestBody.invitedUserName).to.be.a("string");

            //Create many conversation
            cy.conversationEndpoint(requestBody, accessToken, session_Id);
            i++;
        }

        //Get conversations and validate the response body of each conversation
        cy.conversationsEndpoint(accessToken, session_Id)
            .should((response) => {
                expect(response.body.conversations).to.be.an("array");
                for (var conversationIndex in response.body.conversations) {
                    expect(response.body.conversations[conversationIndex]).to.be.an("object");

                    expect(response.body.conversations[conversationIndex]).to.have.property("conversationId");
                    expect(response.body.conversations[conversationIndex].conversationId).to.be.a("string");
                    expect(response.body.conversations[conversationIndex].conversationId).to.match(uuidFormatChecker_UpperCase);

                    expect(response.body.conversations[conversationIndex]).to.have.property("state");
                    expect(response.body.conversations[conversationIndex].state).to.be.a("number");

                    expect(response.body.conversations[conversationIndex]).to.have.property("userA");
                    expect(response.body.conversations[conversationIndex].userA).to.be.an("object");
                    expect(response.body.conversations[conversationIndex].userA).to.have.property("sessionId");
                    expect(response.body.conversations[conversationIndex].userA.sessionId).to.match(uuidFormatChecker_UpperCase);
                    expect(response.body.conversations[conversationIndex].userA).to.have.property("id");
                    expect(response.body.conversations[conversationIndex].userA.id).to.match(uuidFormatChecker_UpperCase);
                    expect(response.body.conversations[conversationIndex].userA).to.have.property("name");
                    expect(response.body.conversations[conversationIndex].userA.name).to.be.a("string");

                    expect(response.body.conversations[conversationIndex]).to.have.property("userB");
                    expect(response.body.conversations[conversationIndex].userB).to.be.an("object");
                    expect(response.body.conversations[conversationIndex].userB).to.have.property("name");
                    expect(response.body.conversations[conversationIndex].userB.name).to.be.a("string");

                    expect(response.body.conversations[conversationIndex]).to.have.property("userARating");
                    expect(response.body.conversations[conversationIndex]).to.have.property("consent");
                    expect(response.body.conversations[conversationIndex]).to.have.property("conversationTimestamp");
                    expect(response.body.conversations[conversationIndex]).to.have.property("alignmentScoresId");
                }
             });
    });

    it("should not allow creating a conversation with an invited_username of 0 characters", () => {
        //Generate a username to be invited
        requestBody = {
        "invitedUserName": ""
        }
        expect(requestBody.invitedUserName).to.be.a("string");

        //Create a conversation and test the response body
        cy.conversationEndpoint(requestBody, accessToken, session_Id).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal(
                "application/json"
            );
            expect(response.body).to.be.an("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === invalidInvitedUsername;
            });
        });
    });

    it("should not allow creating a conversation with an invited_username of 21 characters", () => {
        //Generate a username to be invited
        requestBody = {
            "invitedUserName": "managementmanagementm"
        }
        expect(requestBody.invitedUserName).to.be.a("string");

        //Create a conversation and test the response body
        cy.conversationEndpoint(requestBody, accessToken, session_Id).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal(
                "application/json"
            );
            expect(response.body).to.be.an("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === invalidInvitedUsername;
            });
        });
    });

    it("should not allow creating a conversation with an invited_username greater than 20 characters", () => {
        //Generate a username to be invited
        requestBody = {
        "invitedUserName": "managementmanagementmanagementmanagementmanagementm"
        }
        expect(requestBody.invitedUserName).to.be.a("string");

        //Create a conversation and test the response body
        cy.conversationEndpoint(requestBody, accessToken, session_Id).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal(
                "application/json"
            );
            expect(response.body).to.be.an("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === invalidInvitedUsername;
            });
        });
    });

    it("should not allow creating a conversation without providing a JSON Body containing invited_username", () => {
        //Generate a username to be invited
        invitedUserName = faker.name.firstName();
        
        expect(invitedUserName).to.be.a("string");

        //Create a conversation and test the response body
        cy.conversationEndpoint(invitedUserName, accessToken, session_Id).should((response) => {
            expect(response.status).to.equal(400);
            expect(response.headers["content-type"]).to.equal(
                "application/json"
            );
            expect(response.body).to.be.an("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === missingJSONBodyMessage;
            });
        });
    });

    it("should handle creating conversation with a SESSION_UUID that is not in the db.", () => {
        //Generate a username to be invited
        requestBody = {
            "invitedUserName": `${faker.name.firstName()}`
        };
        expect(requestBody.invitedUserName).to.be.a("string");

        //Seesion UUID not in the DB
        session_Id = "82933689-2561-4211-a27a-058e48721fac"

        //Create a conversation and test the response body
        cy.conversationEndpoint(requestBody, accessToken, session_Id).should((response) => {
            expect(response.status).to.equal(404);
            expect(response.headers["content-type"]).to.equal(
                "application/json"
            );
            expect(response.body).to.be.an("object");
            expect(response.body).to.have.property("error");
            expect(response.body.error).to.be.a("string");
            expect(response.body.error).to.satisfy(function (s) {
                return s === SESSION_UUIDNotInDBMessage;
            });
        });
    });

    it("should get an empty conversations array when no converstion has been created yet", () => {
        //Get conversations and validate the response body
        cy.conversationsEndpoint(accessToken, session_Id)
            .should((response) => {
                expect(response.status).to.equal(200);
                expect(response.headers["content-type"]).to.equal(
                    "application/json"
                );
                expect(response.body).to.deep.equal({
                    "conversations": []
                })
            });
    });
});
