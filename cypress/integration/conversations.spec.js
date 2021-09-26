//  /// <reference types="cypress" />
import scores from "../fixtures/postScores.json";

var faker = require("faker");

let session_Id;
let set_one_quizId;
let user1;
let accessToken;
let invited_username;
let invited_username1 = faker.name.firstName();
let invited_username2 = faker.name.firstName();
let invited_username3 = faker.name.firstName();
let invited_username4 = faker.name.firstName();
let invited_username5 = faker.name.firstName();
let invited_username6 = faker.name.firstName();
let invited_username7 = faker.name.firstName();

describe("'/conversation' endpoint", () => {
    beforeEach(() => {
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
                expect(user1.firstName).to.be.a('string')
                cy.registerEndpoint(user1).should((response) => {
                    expect(response.status).to.equal(201);
                    accessToken = response.body.access_token;
                    expect(response.body.access_token).to.be.a('string')
                });
            });
        });
    });

    it("should create a conversation", () => {
        //Generate a username to be invited
        invited_username = faker.name.firstName()
        expect(invited_username).to.be.a("string");

        //Create a conversation and test the response body
        cy.conversationEndpoint(invited_username, accessToken, session_Id).should((response) => {
            expect(response.status).to.equal(201);
            expect(response.headers["content-type"]).to.equal(
                "application/json"
            );
            expect(response.body).to.be.an("object");
            expect(response.body).to.have.property("message");
            expect(response.body).to.have.property("conversationId");
        });
    });

    it("should get conversations", () => {
        //Create many conversation
        cy.conversationEndpoint(invited_username1, accessToken, session_Id);
        cy.conversationEndpoint(invited_username2, accessToken, session_Id);
        cy.conversationEndpoint(invited_username3, accessToken, session_Id);
        cy.conversationEndpoint(invited_username4, accessToken, session_Id);
        cy.conversationEndpoint(invited_username5, accessToken, session_Id);
        cy.conversationEndpoint(invited_username6, accessToken, session_Id);
        cy.conversationEndpoint(invited_username7, accessToken, session_Id);

        //Get conversations and validate the response body of each conversation
        cy.conversationsEndpoint(accessToken, session_Id)
            .should((response) => {
                expect(response.status).to.equal(200);
                expect(response.body).to.be.an("object");
                expect(response.body).to.have.property("conversations");
                expect(response.body.conversations).to.be.an("array");
                for (var conversationIndex in response.body.conversations) {
                    expect(response.body.conversations[conversationIndex]).to.be.an("object");
                    expect(response.body.conversations[conversationIndex]).to.have.property("conversationId");
                    expect(response.body.conversations[conversationIndex]).to.have.property("conversationStatus");
                    expect(response.body.conversations[conversationIndex]).to.have.property("createdByUserId");
                    expect(response.body.conversations[conversationIndex]).to.have.property("createdDateTime");
                    expect(response.body.conversations[conversationIndex]).to.have.property("invitedUserName");

                    expect(response.body.conversations[conversationIndex].conversationId).to.be.a("string");
                    expect(response.body.conversations[conversationIndex].conversationStatus).to.be.a("number");
                    expect(response.body.conversations[conversationIndex].createdByUserId).to.be.a("string");
                    expect(response.body.conversations[conversationIndex].createdDateTime).to.be.a("string");
                    expect(response.body.conversations[conversationIndex].invitedUserName).to.be.a("string");
                }
            });
    });
});
