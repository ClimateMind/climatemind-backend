// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

Cypress.Commands.add('sessionEndpoint', () => {
    return cy
        .request("POST", "http://localhost:5000/session")
        .then(cy.wrap);
});

Cypress.Commands.add('scoresEndpoint', (scores, session_Id) => {
    return cy
        .request({
            method: 'POST',
            url: 'http://localhost:5000/scores',
            body: scores,
            headers: {
                'content-type': 'application/json',
                'X-Session-Id': session_Id
            },
        })
        .then(cy.wrap);
});

Cypress.Commands.add('personalValuesEndpoint', (quizId) => {
    return cy
        .request({
            method: 'GET',
            url: `http://localhost:5000/personal_values?quizId=${quizId}`,
        })
        .then(cy.wrap);
});

Cypress.Commands.add('questionsEndpoint', () => {
    return cy
        .request({
            method: 'GET',
            url: 'http://localhost:5000/questions',
        })
        .then(cy.wrap);
});

Cypress.Commands.add('registerEndpoint', (user) => {
    return cy
        .request(
            {
                method: 'POST',
                url: "http://localhost:5000/register",
                body: user,
                failOnStatusCode: false,
            }
        )
        .then(cy.wrap);
});

Cypress.Commands.add('logoutEndpoint', () => {
    return cy
        .request("POST", "http://localhost:5000/logout")
        .then(cy.wrap);
});

Cypress.Commands.add('loginEndpoint', (user) => {
    return cy
        .request(
            {
                method: 'POST',
                url: "http://localhost:5000/login",
                body: user,
                failOnStatusCode: false,
            })
        .then(cy.wrap);
});

Cypress.Commands.add('getActionsEndpoint', (effectName) => {
    return cy
        .request({
            method: 'GET',
            url: `http://localhost:5000/get_actions?effect-name=${effectName}`,
        })
        .then(cy.wrap);
});

Cypress.Commands.add('conversationEndpoint', (requestBody, accessToken, session_Id) => {
    return cy
        .request(
            {
                method: 'POST',
                url: "http://localhost:5000/conversation",
                body: requestBody
                ,
                failOnStatusCode: false,
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'X-Session-Id': session_Id
                },
            })
        .then(cy.wrap);
});

Cypress.Commands.add('emailEndpoint', (accessToken) => {
    return cy
        .request({
            method: 'GET',
            url: 'http://localhost:5000/email',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            },
            failOnStatusCode: false,
        })
        .then(cy.wrap);
});

Cypress.Commands.add('updateEmailEndpoint', (accessToken, updateEmailBody) => {
    return cy
        .request({
            method: 'PUT',
            url: 'http://localhost:5000/email',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            },
            body: updateEmailBody,
            failOnStatusCode: false,
        })
        .then(cy.wrap);
});

Cypress.Commands.add('conversationsEndpoint', (accessToken, session_Id) => {
    return cy
        .request({
            method: 'GET',
            url: 'http://localhost:5000/conversations',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'X-Session-Id': session_Id
            },
            failOnStatusCode: false,
        })
        .then(cy.wrap);
});
