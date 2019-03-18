'use strict';

// Define class
class DailyAllowanceNumber extends React.Component {
  constructor(props) {
    super(props);
    // There's no real need to set state because we don't modify the value of of allowanceNumber
    // this.state = {
    //     // We can name attributes of the state object whatever we want
    //     // Naming it allowanceNumber to be consistent with prop name
    //     allowanceNumber: this.props.allowanceNumber
    // }
  }

  getTextColor() {
      return (this.props.allowanceNumber > 25) ? 'red' : 'white';
  }

  render() {
      // console.log("Props:")
      // console.log(this.props)
      // console.log("State:")
      // console.log(this.state)
      return (
          <div style={{ color: this.getTextColor() }}>
              { this.props.allowanceNumber }
          </div>
      )
  }
}

// Define what to render
// Get the element to render the component into
const element = document.querySelector('#daily_allowance_number')
// https://reactjs.org/docs/react-dom.html#render
// ReactDOM.render(Component, Container)
ReactDOM.render(
  // Element to render (the Component)
  <DailyAllowanceNumber
    allowanceNumber={
        // Get the value attribute from the specified element
        element.getAttribute('value')
    }
  />,
  // Container to render it in (div in user_dashboard.html with id #daily_allowance_number)
  element
);