export const getFederatedLearningJobSseUrl = () => {
    return '/api_federated_learning_management/jobs/sse'
}

export const getChatSseUrl = (userId: string) => {
    return `/api_chat/chats/sse/${userId}`
}