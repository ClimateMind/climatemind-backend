/// <reference types="cypress" />

const user1 = {
  full-name: "user one",
  email: "test1@example.com",
  password: "PassWord7!",
};

const user2 = {
  full-name: "user two",
  email: "test2@example.com",
  password: "PassWord7!",
};

const successMessage = "Succesfully created user";
const badReqMessage = "email and password must be included in request body";
const alreadyRegisteredMessage = "Email already regsitered";

describe("User Registration", () => {
  it("It can register a user", () => {
    cy.request("POST", "http://localhost:5000/register", user1).should(
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

  it("Can regsiter another user", () => {
    cy.request("POST", "http://localhost:5000/register", user2).should(
      (response) => {
        expect(response.status).to.equal(201);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("message");
        expect(response.body.Message).to.satisfy(function (s) {
          return s === successMessage;
        });
      }
    );
  });
  it("It handles if the user already exists", () => {
    cy.request("POST", "http://localhost:5000/register", user2).should(
      (response) => {
        expect(response.status).to.equal(401);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.Message).to.satisfy(function (s) {
          return s === alreadyRegisteredMessage;
        });
      }
    );
  });

  it("It handles a missing email", () => {
    const body = {
      password: "password",
    };
    cy.request("POST", "http://localhost:5000/register", body).should(
      (response) => {
        expect(response.status).to.equal(400);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.Message).to.satisfy(function (s) {
          return s === badReqMessage;
        });
      }
    );
  });

  it("It handles a missing password", () => {
    const body = {
      email: "missingpassword@example.com",
    };
    cy.request("POST", "http://localhost:5000/register", body).should(
      (response) => {
        expect(response.status).to.equal(400);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.Message).to.satisfy(function (s) {
          return s === badReqMessage;
        });
      }
    );
  });

  it("It handles a missing body", () => {
    cy.request("POST", "http://localhost:5000/register").should((response) => {
      expect(response.status).to.equal(400);
      expect(response.headers["content-type"]).to.equal("application/json");
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("error");
      expect(response.body.Message).to.satisfy(function (s) {
        return s === badReqMessage;
      });
    });
  });
});
