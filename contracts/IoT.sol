pragma solidity ^0.5.0;

contract IoT {
  uint public taskCount = 0;

  struct Task {
    uint id;
    string timestamp;
    string desc;
    string entityType;
    uint v1;
    uint v2;
    uint v3;
    uint latitude;
    uint longitude;
  }

  mapping(uint => Task) public tasks;

  event TaskCreated(
    uint id,
    string timestamp,
    string desc,
    string entityType,
    uint v1,
    uint v2,
    uint v3,
    uint latitude,
    uint longitude
  );

  event TaskCompleted(
    uint id,
    bool completed
  );

  constructor() public {
    createTask(1, "Timestamp: Today Baby Jarvis", "Test desc", "Test entity type", 1, 2, 3, 1, 2);
  }

  function createTask(uint _id, string memory _timestamp, string memory _desc, string memory _entityType, uint _v1, uint _v2, uint _v3, uint _latitude, uint _longitude) public {
    taskCount ++;
    tasks[taskCount] = Task(_id, _timestamp, _desc, _entityType, _v1, _v2, _v3, _latitude, _longitude);
    emit TaskCreated(_id, _timestamp, _desc, _entityType, _v1, _v2, _v3, _latitude, _longitude);
  }

  function toggleCompleted(uint _id) public {
    //Task memory _task = tasks[_id];
    //_task.completed = !_task.completed;
    //tasks[_id] = _task;
    //emit TaskCompleted(_id, _task.completed);
  }

}
