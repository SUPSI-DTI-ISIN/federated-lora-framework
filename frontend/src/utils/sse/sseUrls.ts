export const getFederatedLearningJobSseUrl = () => {
    return '/api_federated_learning_management/jobs/sse'
}

export const getChatSseUrl = (basePath: string, userId: string) => {
    return `${basePath}/api_chat/chats/sse/${userId}`
}