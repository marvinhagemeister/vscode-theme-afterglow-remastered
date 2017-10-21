export function Text() {
  return (
    <div>
      <Heading text="foo">Hello World</Heading>
      <p>Lorem Ipsum</p>
      <div>The End</div>
    </div>
  );
}

export function Heading(props) {
  return (
    <h1>
      {props.text} - {props.children}
    </h1>
  );
}
