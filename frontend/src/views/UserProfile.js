import React from "react";

// react-bootstrap components
import {Button, Card, Col, Container, Form, Row,} from "react-bootstrap";
import {BootstrapTable, TableHeaderColumn} from "react-bootstrap-table";

class User extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: "389801252"
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({value: event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();
        let url = `http://127.0.0.1:8000/reviews/${this.state.value}/`;
        fetch(url)
            .then((res) => res.json())
            .then((json) => {
                this.setState({
                    data: json,
                });
            }).catch(e => alert(e));
    }

    render() {
        return (
            <Container fluid>
                <Row>
                    <Col md="12">
                        <Card>
                            <Card.Header>
                                <Card.Title as="h4">Enter Application App Store ID</Card.Title>
                            </Card.Header>
                            <Card.Body>
                                <Form>
                                    <Row>
                                        <Col className="pr-1" md="12">
                                            <Form.Group>
                                                <label>App ID</label>
                                                <Form.Control
                                                    defaultValue=""
                                                    placeholder="389801252"
                                                    type="text"
                                                    onChange={this.handleChange}
                                                />
                                            </Form.Group>
                                        </Col>
                                    </Row>
                                    <Button
                                        className="btn-fill pull-right a"
                                        type="submit"
                                        variant="primary"
                                        onClick={this.handleSubmit}
                                    >
                                        Get App Reviews
                                    </Button>
                                    <div className="clearfix"></div>
                                </Form>
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col></Col>
                </Row>
                <Row>
                    <Col md="12">
                        <BootstrapTable data={this.state.data} striped hover>
                            <TableHeaderColumn isKey dataField='id'>ID</TableHeaderColumn>
                            <TableHeaderColumn dataField='content'>content</TableHeaderColumn>
                            <TableHeaderColumn dataField='informative' filter={{
                                type: 'SelectFilter',
                                options: {false: false, true: true}
                            }}>Informative</TableHeaderColumn>
                            <TableHeaderColumn dataField='bugReport'
                                               filter={{type: 'SelectFilter', options: {false: false, true: true}}}>Bug
                                Report</TableHeaderColumn>
                            <TableHeaderColumn dataField='featureRequest'
                                               filter={{type: 'SelectFilter', options: {false: false, true: true}}}>Feature
                                Request</TableHeaderColumn>
                            <TableHeaderColumn dataField='praise' filter={{
                                type: 'SelectFilter',
                                options: {false: false, true: true}
                            }}>Praise</TableHeaderColumn>
                            <TableHeaderColumn dataField='critic' filter={{
                                type: 'SelectFilter',
                                options: {false: false, true: true}
                            }}>Critic</TableHeaderColumn>
                        </BootstrapTable>
                    </Col>
                </Row>

            </Container>
        );
    }
}

export default User;