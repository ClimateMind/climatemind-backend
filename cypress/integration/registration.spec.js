/// <reference types="cypress" />

const user1 = {
  email: "test1@example.com",
  password: "password",
};

const user2 = {
  email: "test2@example.com",
  password: "password",
};

describe("User Registration", () => {
  it("It can register a user", () => {
    cy.request("POST", "http://localhost:5000/register", user1).should(
      (response) => {
        expect(response.status).to.equal(201);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("message");
        expect(response.body.Message).to.satisfy(function (s) {
          return s === "Succesfully created user";
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
          return s === "Succesfully created user";
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
          return s === "Email already regsitered";
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
          return s === "email and password must be included in request body";
        });
      }
    );
  });

  it("It handles a missing password", () => {
    const body = {
      email: "test3@example.com",
    };
    cy.request("POST", "http://localhost:5000/register", body).should(
      (response) => {
        expect(response.status).to.equal(400);
        expect(response.headers["content-type"]).to.equal("application/json");
        expect(response.body).to.be.a("object");
        expect(response.body).to.have.property("error");
        expect(response.body.Message).to.satisfy(function (s) {
          return s === "email and password must be included in request body";
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
        return s === "email and password must be included in request body";
      });
    });
  });
});
