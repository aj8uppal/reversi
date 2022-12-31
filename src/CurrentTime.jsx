import React from 'react';

const WorldCupClock = () => {
  const [time, setTime] = React.useState(new Date());

  // Get the current time in the city that the 2022 World Cup is being held in
  const worldCupTime = new Date(time.getTime() + (time.getTimezoneOffset() - 240) * 60000);

  // Update the time every minute
  React.useEffect(() => {
    const interval = setInterval(() => setTime(new Date()), 60000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>Current Time:</h1>
      <p>{time.toLocaleTimeString()}</p>
      <h1>World Cup Time:</h1>
      <p>{worldCupTime.toLocaleTimeString()}</p>
    </div>
  );
};

export default WorldCupClock;