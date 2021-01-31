/// <reference types="cypress" />

describe("/questions endpoint", () => {
  it("GET Questions", () => {
    cy.request("http://localhost:5000/questions").should((response) => {
      expect(response.status).to.equal(200);
      expect(response.headers["content-type"]).to.equal("application/json");
      expect(response.headers["access-control-allow-origin"]).to.equal("*");
      expect(response.body).to.have.property("SetOne");
      expect(response.body).to.have.property("SetTwo");
      expect(response.body).to.have.property("Answers");
      expect(response.body.SetOne).to.have.length(10);
      expect(response.body.SetTwo).to.have.length(10);
      expect(response.body.Answers).to.have.length(6);
    });
  });

  it("SetOne has the correct properties", () => {
    cy.request("http://localhost:5000/questions").should((response) => {
      const SetOne = response.body.SetOne;
      SetOne.forEach((question) => {
        expect(question).to.have.property("id");
        expect(question).to.have.property("question");
        expect(question).to.have.property("value");
        expect(question.id).to.be.a("number");
        expect(question.question).to.be.a("string");
        expect(question.value).to.be.a("string");
      });
    });
  });
  it("SetTwo has the correct properties", () => {
    cy.request("http://localhost:5000/questions").should((response) => {
      const SetTwo = response.body.SetOne;
      SetTwo.forEach((question) => {
        expect(question).to.have.property("id");
        expect(question).to.have.property("question");
        expect(question).to.have.property("value");
        expect(question.id).to.be.a("number");
        expect(question.question).to.be.a("string");
        expect(question.value).to.be.a("string");
      });
    });
  });
  it("Answers has the correct properties", () => {
    cy.request("http://localhost:5000/questions").should((response) => {
      const Answers = response.body.Answers;
      Answers.forEach((answer) => {
        expect(answer).to.have.property("id");
        expect(answer).to.have.property("text");
        expect(answer.id).to.be.a("number");
        expect(answer.text).to.be.a("string");
      });
    });
  });
});
