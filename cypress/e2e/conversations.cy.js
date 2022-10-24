//  /// <reference types="cypress" />
import scores from "../fixtures/postScores.json";

var faker = require("faker");

let session_Id;
let set_one_quizId;
let user;
let accessToken;
const missingJSONBodyMessage = "Must provide a JSON body with the name of the invited user.";
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

});
