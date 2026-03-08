interface TableSkeletonProps {
    count: number;
}

export const TableSkeleton = ({count}: TableSkeletonProps) => {
    const items = Array.from({length: count}, (_, i) => i);

    return (
        <div className="overflow-x-auto rounded-lg bg-base-100 shadow" role="status" aria-label="Loading content">
            <table className="table w-full">
                <thead>
                <tr>
                    <th>
                        <div className="h-4 w-24 animate-pulse rounded bg-base-300"/>
                    </th>
                    <th>
                        <div className="h-4 w-20 animate-pulse rounded bg-base-300"/>
                    </th>
                    <th>
                        <div className="h-4 w-16 animate-pulse rounded bg-base-300"/>
                    </th>
                    <th>
                        <div className="h-4 w-16 animate-pulse rounded bg-base-300"/>
                    </th>
                    <th>
                        <div className="h-4 w-20 animate-pulse rounded bg-base-300"/>
                    </th>
                </tr>
                </thead>
                <tbody>
                {items.map((i) => (
                    <tr key={i}>
                        <td>
                            <div className="flex items-center gap-3">
                                <div className="h-8 w-8 flex-shrink-0 animate-pulse rounded bg-base-300"/>
                                <div className="h-4 w-32 animate-pulse rounded bg-base-300"/>
                            </div>
                        </td>
                        <td>
                            <div className="h-6 w-16 animate-pulse rounded-full bg-base-300"/>
                        </td>
                        <td>
                            <div className="h-4 w-20 animate-pulse rounded bg-base-300"/>
                        </td>
                        <td>
                            <div className="h-4 w-16 animate-pulse rounded bg-base-300"/>
                        </td>
                        <td>
                            <div className="flex gap-2">
                                <div className="h-8 w-8 animate-pulse rounded-lg bg-base-300"/>
                                <div className="h-8 w-8 animate-pulse rounded-lg bg-base-300"/>
                            </div>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
            <span className="sr-only">Loading...</span>
        </div>
    );
}
