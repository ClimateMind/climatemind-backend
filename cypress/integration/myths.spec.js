/// <reference types="cypress" />

describe("/myths endpoint", () => {
  it("GET Myths", () => {
    cy.request("http://localhost:5000/myths").should((response) => {
      expect(response.status).to.equal(200);
      expect(response.headers["content-type"]).to.equal("application/json");
      expect(response.headers["access-control-allow-origin"]).to.equal("*");
      expect(response.body).to.be.a("object");
      expect(response.body).to.have.property("myths");
      expect(response.body.myths).to.not.have.length(0);
      expect(response.body.myths).first().to.not.have.length(0);
      expect(response.body.myths).first().to.have.property("faultyLogicDescription");
      expect(response.body.myths).first().to.have.property("iri");
      expect(response.body.myths).first().to.have.property("mythClaim");
      expect(response.body.myths).first().to.have.property("mythRebuttal");
      expect(response.body.myths).first().to.have.property("mythSources");
      expect(response.body.myths).first().to.have.property("mythTitle");
      expect(response.body.myths).first().to.have.property("mythVideos");
    });
  });
  
  it("Each myth has the correct properties", () => {
    cy.request("http://localhost:5000/myths").should((response) => {
      const myths = response.body.myths;
      myths.forEach((myth) => {
        expect(myth).to.have.property("faultyLogicDescription");
        expect(myth).to.have.property("iri");
        expect(myth).to.have.property("mythClaim");
        expect(myth).to.have.property("mythRebuttal");
        expect(myth).to.have.property("mythSources");
        expect(myth).to.have.property("mythTitle");
        expect(myth).to.have.property("mythVideos");
        expect(myth.faultyLogicDescription).to.be.a("string");
        expect(myth.iri).to.be.a("string");
        expect(myth.mythClaim).to.be.a("string");
        expect(myth.mythRebuttal).to.be.a("string");
        expect(myth.mythSources).to.be.a("array");
        expect(myth.mythTitles).to.be.a("string");
        expect(myth.mythVideos).to.be.a("array")
      });
    });
  });
});
