from box_sdk_gen import BoxClient, User, File, Task, TaskAssignment

from box_sdk_gen.managers.tasks import (
    CreateTaskItem,
    CreateTaskItemTypeField,
    CreateTaskAction,
    CreateTaskCompletionRule,
)

from box_sdk_gen.managers.task_assignments import (
    CreateTaskAssignmentTask,
    CreateTaskAssignmentTaskTypeField,
    CreateTaskAssignmentAssignTo,
)


def create_file_task(
    client: BoxClient, file_id: File, user_id: User, message: str
) -> TaskAssignment:
    task: Task = client.tasks.create_task(
        CreateTaskItem(type=CreateTaskItemTypeField.FILE.value, id=file_id),
        action=CreateTaskAction.REVIEW.value,
        message=message,
        completion_rule=CreateTaskCompletionRule.ANY_ASSIGNEE,
    )

    task_assignment: TaskAssignment = (
        client.task_assignments.create_task_assignment(
            CreateTaskAssignmentTask(
                type=CreateTaskAssignmentTaskTypeField.TASK,
                id=task.id,
            ),
            CreateTaskAssignmentAssignTo(id=user_id),
        )
    )

    return task_assignment
