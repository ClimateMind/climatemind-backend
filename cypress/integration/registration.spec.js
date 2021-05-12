/// <reference types="cypress" />

const user1 = {
  fullname: "user one",
  email: "test1@example.com",
  password: "PassWord7!",
};

const user2 = {
  fullname: "user two",
  email: "test2@example.com",
  password: "PassWord7!",
};

const successMessage = "Successfully created user";
const badReqMessage = "Email and password must included in the request body";
const alreadyRegisteredMessage = "Email already registered";

describe("User Registration", () => {
  it("It can register a user", () => {
    cy.request("POST", "http://localhost:5000/register", user1).should(
      (response) => {
        expect(response.status).to.equal(201);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.headers["access-control-allow-origin"]).to.equal("*");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("message");
        expect(response.body.message).to.satisfy(function (s) {
          return s === successMessage;
        });
      }
    );
  });

  it("Can register another user", () => {
    cy.request("POST", "http://localhost:5000/register", user2).should(
      (response) => {
        expect(response.status).to.equal(201);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("message");
        expect(response.body.message).to.satisfy(function (s) {
          return s === successMessage;
        });
      }
    );
  });
  it("It handles if the user already exists", () => {
    cy.request({
        url: "http://localhost:5000/register",
        method: "POST",
        body: user2,
        failOnStatusCode: false
    }).should(
      (response) => {
        expect(response.status).to.equal(401);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.satisfy(function (s) {
          return s === alreadyRegisteredMessage;
        });
      }
    );
  });

  it("It handles a missing email", () => {
    const body = {
      fullname: "test user",
      password: "password",
    };
    cy.request({
        url: "http://localhost:5000/register",
        method: "POST",
        body: body,
        failOnStatusCode: false
    }).should(
      (response) => {
        expect(response.status).to.equal(400);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.satisfy(function (s) {
          return s === badReqMessage;
        });
      }
    );
  });

  it("It handles a missing password", () => {
    const body = {
      fullname: "test user",
      email: "missingpassword@example.com",
    };
    cy.request({
        url: "http://localhost:5000/register",
        method: "POST",
        body: body,
        failOnStatusCode: false
    }).should(
      (response) => {
        expect(response.status).to.equal(400);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.error).to.satisfy(function (s) {
          return s === badReqMessage;
        });
      }
    );
  });

  it("It handles a missing body", () => {
    cy.request({
        url: "http://localhost:5000/register",
        method: "POST",
        failOnStatusCode: false
    }).should((response) => {
      expect(response.status).to.equal(400);
      expect(response.headers["content-type"]).to.equal("application/json");
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("error");
      expect(response.body.error).to.satisfy(function (s) {
        return s === badReqMessage;
      });
    });
  });
});
