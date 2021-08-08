/// <reference types="cypress" />

describe("/get_actions endpoint", () => {
    it("should get actions", () => {
        cy.request("GET","http://localhost:5000/get_actions?effect-name=increase in flooding of land and property").should((response) => {
            expect(response.status).to.equal(200);
            expect(response.headers["content-type"]).to.equal("application/json");
            expect(response.headers["access-control-allow-origin"]).to.equal("*");
            expect(response.body).to.be.a("object");
            expect(response.body).to.have.property("actions");
            expect(response.body.actions).to.not.have.length(0);
        });
    });

    it("Each action has the correct properties", () => {
        cy.request("http://localhost:5000/get_actions?effect-name=increase in flooding of land and property").should((response) => {
            const solutions = response.body.actions;
            solutions.forEach((solution) => {
                expect(solution).to.have.property("imageUrl");
                expect(solution).to.have.property("iri");
                expect(solution).to.have.property("longDescription");
                expect(solution).to.have.property("shortDescription");
                expect(solution).to.have.property("solutionSources");
                expect(solution).to.have.property("solutionSpecificMythIRIs");
                expect(solution).to.have.property("solutionTitle");
                expect(solution).to.have.property("solutionType");

                expect(solution.imageUrl).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(solution.iri).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(solution.longDescription).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(solution.shortDescription).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(solution.solutionSources).to.satisfy(function (s) {
                    return s === null || Array.isArray(s)
                });
                expect(solution.solutionSpecificMythIRIs).to.satisfy(function (s) {
                    return s === null || Array.isArray(s)
                });
                expect(solution.solutionTitle).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
                expect(solution.solutionType).to.satisfy(function (s) {
                    return s === null || typeof s == 'string'
                });
            });
        });
    });
});